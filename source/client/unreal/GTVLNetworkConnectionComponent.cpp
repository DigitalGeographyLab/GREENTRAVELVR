// Fill out your copyright notice in the Description page of Project Settings.


#include "GTVLNetworkConnectionComponent.h"
#include "WebSocketsModule.h"
#include "Json.h"
#include "JsonUtilities.h"

// Initialize the static WebSocket pointer to nullptr
TSharedPtr<IWebSocket> UGTVLNetworkConnectionComponent::WebSocket = nullptr;

// Sets default values for this component's properties
UGTVLNetworkConnectionComponent::UGTVLNetworkConnectionComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	lastCrankRevValue = MIN_flt;
	lastThrottleValue = 0.0f;

	if (!WebSocket.IsValid()) {
		WebSocket = FWebSocketsModule::Get().CreateWebSocket("ws://127.0.0.1:8080");
	}
	if(WebSocket.IsValid() && !WebSocket->IsConnected())
	{
		// Add all the necessary callbacks on the WebSocket
		WebSocket->OnConnected().AddUObject(this, &UGTVLNetworkConnectionComponent::OnWebSocketConnected);
		WebSocket->OnConnectionError().AddUObject(this, &UGTVLNetworkConnectionComponent::OnWebSocketConnectionError);
		WebSocket->OnClosed().AddUObject(this, &UGTVLNetworkConnectionComponent::OnWebSocketClosed);
		WebSocket->OnMessage().AddUObject(this, &UGTVLNetworkConnectionComponent::OnWebSocketMessage);
		WebSocket->Connect();

		// Lambdas can also be added.
		WebSocket->OnMessageSent().AddLambda([](const FString& MessageString) {
			//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, "Sent Message: " + MessageString);
			});
		WebSocket->Connect();
		FString DataToSend = "Hello From Unreal, WebSocket Server!";
		WebSocket->Send(TCHAR_TO_UTF8(*DataToSend), DataToSend.Len());
	}
}


// Called when the game starts
void UGTVLNetworkConnectionComponent::BeginPlay()
{
	Super::BeginPlay();

	// ...
	if (!FModuleManager::Get().IsModuleLoaded("WebSockets"))
	{
		FModuleManager::Get().LoadModule("WebSockets");
	}
}

void UGTVLNetworkConnectionComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (WebSocket.IsValid() && WebSocket->IsConnected())
	{
		WebSocket->Close();
	}

	Super::EndPlay(EndPlayReason);
}

// Called every frame
void UGTVLNetworkConnectionComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
}

void UGTVLNetworkConnectionComponent::OnWebSocketMessage(const FString& MessageString)
{
	// Handle incoming WebSocket message
	// Assuming the message is a JSON object with a throttle value
	int32 JsonStartIndex;
	if (MessageString.FindChar('{', JsonStartIndex))
	{
		// Extract the JSON part of the message
		FString JsonString = MessageString.Mid(JsonStartIndex);
		TSharedPtr<FJsonObject> JsonObject;
		TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

		if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
		{
			FString typeString = JsonObject->GetStringField("type");
			FString actionString = JsonObject->GetStringField("action");
			if (!typeString.IsEmpty() && typeString.Len() > 0 && typeString.Contains(TEXT("dashboard")) &&
				!actionString.IsEmpty() && actionString.Len() > 0 && actionString.Contains(TEXT("statuscheck")))
			{
				// Create a new JSON object, put our message, deserialize into a string and send back.
				TSharedPtr<FJsonObject> JsonWriterObject = MakeShareable(new FJsonObject());
				JsonWriterObject->SetStringField(TEXT("type"), TEXT("ue5"));
				JsonWriterObject->SetStringField(TEXT("action"), TEXT("statuscheck"));

				FString OutputString;
				TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&OutputString);
				FJsonSerializer::Serialize(JsonWriterObject.ToSharedRef(), Writer);

				// Send to the server.
				WebSocket->Send(TCHAR_TO_UTF8(*OutputString), OutputString.Len());
			}
			else if (!typeString.IsEmpty() && typeString.Len() > 0 && typeString.Contains(TEXT("bike")))
			{
				FString crankRevString = JsonObject->GetStringField("cumulative_crank_revs");
				FString crankTimeString = JsonObject->GetStringField("last_crank_event_time");

				if (!crankRevString.IsEmpty() && crankRevString.Len() > 0)
				{
					float floatVal = FCString::Atof(*crankRevString);
					if (floatVal > lastCrankRevValue) {
						lastThrottleValue = 1.0;
					}
					else
					{
						lastThrottleValue = 0.0f;
					}

					OnMessageReceived.Broadcast("throttle", FString::SanitizeFloat(lastThrottleValue));

					lastCrankRevValue = floatVal;
				}
			}
			else
			{
				FString throttleString = JsonObject->GetStringField("throttle");
				FString steeringString = JsonObject->GetStringField("steering");

				if (!throttleString.IsEmpty() && throttleString.Len() > 0)
				{
					OnMessageReceived.Broadcast("throttle", throttleString);
				}
				// Steering Code is not used for GreenTravel
				if (!steeringString.IsEmpty() && steeringString.Len() > 0) {
					float floatVal = FCString::Atof(*steeringString);
					// convert the value in the range of -1 to 1
					floatVal = -(floatVal / 100.0f);
					steeringString = FString::SanitizeFloat(floatVal);
					OnMessageReceived.Broadcast("steering", steeringString);
				}
			}
		}
	}

}

/// <summary>
/// We use this to tell the server when any checkpoint blueprint is crossed.
/// </summary>
/// <param name="whichCheckPoint"></param>
void UGTVLNetworkConnectionComponent::CheckPointCrosssed(const FString& whichCheckPoint)
{
	if (WebSocket->IsConnected())
	{
		// Create a new JSON object, put our message, deserialize into a string and send back.
		TSharedPtr<FJsonObject> JsonWriterObject = MakeShareable(new FJsonObject());
		JsonWriterObject->SetStringField(TEXT("type"), TEXT("ue5"));
		JsonWriterObject->SetStringField(TEXT("action"), TEXT("checkpoint"));
		JsonWriterObject->SetStringField(TEXT("message"), whichCheckPoint);

		FString OutputString;
		TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&OutputString);
		FJsonSerializer::Serialize(JsonWriterObject.ToSharedRef(), Writer);

		// Send to the server.
		WebSocket->Send(TCHAR_TO_UTF8(*OutputString), OutputString.Len());
	}
}

void UGTVLNetworkConnectionComponent::OnWebSocketConnected()
{
	// Handle WebSocket connected
	//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Green, "Successfully Connected To Server");

}

void UGTVLNetworkConnectionComponent::OnWebSocketConnectionError(const FString& Error)
{
	// Handle WebSocket connection error
	//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Red, Error);

}

void UGTVLNetworkConnectionComponent::OnWebSocketClosed(int32 StatusCode, const FString& Reason, bool bWasClean)
{
	// Handle WebSocket closed
	//GEngine->AddOnScreenDebugMessage(-1, 15.0f, bWasClean ? FColor::Green : FColor::Red, "Connection Closed" + Reason);

}
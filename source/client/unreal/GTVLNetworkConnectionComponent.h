// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "IWebSocket.h"
#include "GTVLNetworkConnectionComponent.generated.h"


DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FMessageReceivedDelegate, const FString&, str1, const FString&, str2);
UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class BRUSSELSUE5_4_API UGTVLNetworkConnectionComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UGTVLNetworkConnectionComponent();
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	// We want only one websocket, to avoid multiple messages to server.
	static TSharedPtr<IWebSocket> WebSocket;
	// WebSocket Methods
	void OnWebSocketConnected();
	void OnWebSocketConnectionError(const FString& Error);
	void OnWebSocketClosed(int32 StatusCode, const FString& Reason, bool bWasClean);
	void OnWebSocketMessage(const FString& Message);

	float lastCrankRevValue;
	float lastThrottleValue;

	UPROPERTY(BlueprintAssignable, Category = "Events")
	FMessageReceivedDelegate OnMessageReceived;

	// Function to handle the logic of checkpoint crossing
	UFUNCTION(BlueprintCallable, Category = "Checkpoint-Eventsw")
	void CheckPointCrosssed(const FString& whichCheckPoint);

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
};

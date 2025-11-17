# Contributing to GREENTRAVELVR

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at <https://github.com/DigitalGeographyLab/GREENTRAVELVR/issues>.

If you are reporting a bug, please include:

- Your operating system name and version.
- Your Unreal Engine version and VR hardware (headset, trainer, sensors, etc.).
- Any details about your local setup (Python / Node.js versions, OS, Biopac/AcqKnowledge version, etc.) that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with `"bug"` and `"help wanted"` is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for feature requests. Anything tagged with `"enhancement"` and `"help wanted"` is open to whoever wants to implement it.

Examples of useful contributions:

- Improving the network module (e.g. better error handling, more robust reconnection).
- Enhancing the dashboard UI.
- Adding optional modules (e.g. steering / ESP32, additional sensors).
- Improving Unreal-side integration or Blueprint / C++ components.

### Write Documentation

GREENTRAVELVR could always use more documentation, for example:

- Developer documentation in `docs/`.
- Comments and docstrings in Python, C++, and JavaScript files under `source/`.
- How-to guides or blog posts describing how to set up and extend the system.

### Submit Feedback

The best way to send feedback is to file an issue at  
<https://github.com/DigitalGeographyLab/GREENTRAVELVR/issues>.

If you are proposing a feature:

- Explain in detail how it would work and which part of the system it touches (Unreal, network module, sensors, dashboard, etc.).
- Keep the scope as narrow as possible, to make it easier to implement and review.
- Remember that this is a research-driven, mostly volunteer project, and that contributions are welcome 🙂

---

## Get Started!

Ready to contribute? Here's how to set up **GREENTRAVELVR** for local development.

1.  **Fork** the `GREENTRAVELVR` repo on GitHub.

2.  **Clone your fork** locally:

    ```bash
    git clone git@github.com:your_name_here/GREENTRAVELVR.git
    cd GREENTRAVELVR
    ```

3.  **Set up the environment**
    Follow the installation steps in `README.md` (network server, dashboard, Unreal project, Biopac integration). In addition, for development you will typically need:
    * A recent Python 3 (for the bike / Biopac client scripts).
    * Node.js (for the WebSocket server and dashboard).
    * Unreal Engine 5 (for the VR environment and C++ component).
    * Access to the relevant hardware (Garmin Cadence sensor, Biopac/AcqKnowledge, etc.) if you are testing end-to-end.

4.  **Create a branch** for local development:

    ```bash
    git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

5.  **Run checks and tests**
    This repository currently contains multiple technologies (Python, C++, JavaScript/Node, HTML). Before opening a pull request, try to:
    * Run any existing scripts or tests related to the part you modified.
    * For Python changes, consider adding small tests (e.g. with `pytest`) or at least a simple script to exercise your changes.
    * For Node.js changes (e.g. `server.js` or dashboard), start the server and check the browser dashboard behaves as expected.
    * For Unreal changes, build the project and verify that the environment runs and connects properly to the network module.
    * If you introduce a new testing setup (for example, a `tests/` folder with `pytest` or a simple Node test script), document how to run it in the `docs/` folder or in `README.md`.

6.  **Commit your changes** and push your branch to GitHub:

    ```bash
    git add .
    git commit -m "Describe your change briefly, e.g. 'Improve network reconnection logic'"
    git push origin name-of-your-bugfix-or-feature
    ```

7.  **Submit a pull request** through the GitHub website from your branch to the `main` branch of `DigitalGeographyLab/GREENTRAVELVR`.

## Pull Request Guidelines

Before you submit a pull request(PR), check that it meets these guidelines:

* **Clear scope:** The PR should focus on a single bugfix or feature where possible.
* **Tests / verification:**
    * If feasible, include tests (Python unit tests, small integration scripts, or Unreal sample maps / blueprints that exercise the new behavior).
    * At minimum, describe how you manually tested the change (e.g. “Ran bike + server + Unreal, verified cadence values are received correctly”).
* **Documentation updated:**
    * If the pull request adds or changes functionality, update the relevant documentation:
    * Add or update comments/docstrings in the affected files.
    * Update `README.md` and/or files under `docs/` with setup or usage changes.
* **Code style:**
    * Follow the existing style in the surrounding files (Python, C++, and JS).
    * For Python, tools such as `black` or `flake8` are welcome if they do not cause massive unrelated changes.
* **Compatibility:**
    * Make sure the changes work with the toolchain and versions mentioned in `README.md` (Unreal version, Python 3, Node.js, etc.).
    * Avoid introducing dependencies that are difficult to install on typical research machines without a strong reason.
* The maintainers might ask for small changes (naming, structure, or documentation) before merging.

## Tips

To work on specific parts of the system:

* **Network / server module:**
    * Focus on `source/server`, `source/client`, and the dashboard in `source/dashboard`. You can use the mock client mentioned in `README.md` to test message passing without full hardware.
* **Unreal integration:**
    * Focus on the `GTVLNetworkConnectionComponent` C++ class and related Blueprints. Make sure the Unreal project builds and that log messages show a healthy connection to the WebSocket server.
* **Sensor / Biopac integration:**
    * Work in the Python scripts under `source/client/bike` and `source/client/biopac`, and test with the appropriate hardware or simulated data.

## Releasing / Maintaining

This section is mainly for maintainers.

When you are preparing a new “release” of GREENTRAVELVR (for example, for an experiment round, a thesis milestone, or sharing with external collaborators):

1.  Make sure all changes are committed and pushed, and that:
    * `README.md` reflects the current setup process.
    * Any diagrams or documentation in `docs/` are up to date.
2.  Tag the state of the repository with a descriptive Git tag, for example:

    ```bash
    git tag -a v0.2-experiment1 -m "Version used in [short description of experiment]"
    git push --tags
    ```

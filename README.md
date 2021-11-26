# Test Addon

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]

![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports i386 Architecture][i386-shield]

[![Github Actions][github-actions-shield]][github-actions]
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

Example add-on by Community Home Assistant add-ons.

## About

This is an example add-on for Home Assistant. When started, it displays a
random quote every 5 seconds.

It shows off several features and structures like:

- Full blown GitHub repository.
- General Dockerfile structure and setup.
- The use of the `config.json` and `build.json` files.
- General structure on how to use S6 overlay with services.
- Basic usage of Bashio.
- Continuous integration and deployment using GitHub Actions.
- Deployment to the GitHub Container registry.
- Small use of the Bash function library in our base images.
- The use of Docker label schema.

# Python frontend for ROS 2 Launch

The package [`launch`](https://docs.ros.org/en/rolling/p/launch/) is the implementation, the "plumbing" of the ROS 2 launch system.

[XML](https://docs.ros.org/en/humble/p/launch_xml/) and [YAML](https://docs.ros.org/en/humble/p/launch_yaml/) on the other hand are _frontends_ to launch.
That is, they are the intended user-facing API.
However, much of the community got hooked on Python launchfiles due to early adoption when the frontends were incomplete.
With that in mind, and the extensive explicit use of exact filenames and `PythonLaunchDescriptionSource`, migration to these frontends is difficult for packages with downstream consumers.

Enter `launch_frontend_py` - this package provides a Python-language frontend to `launch`, with identical usage to the XML and YAML versions.
It provides the same benefits of conciseness, declarative style, while allowing launchfiles to stay in Python.


## Usage

TODO

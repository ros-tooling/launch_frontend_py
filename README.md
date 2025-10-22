# Python frontend for ROS 2 Launch

The package [`launch`](https://docs.ros.org/en/rolling/p/launch/) is the implementation, the "plumbing" of the ROS 2 launch system.

[XML](https://docs.ros.org/en/humble/p/launch_xml/) and [YAML](https://docs.ros.org/en/humble/p/launch_yaml/) on the other hand are _frontends_ to launch.
That is, they are the intended user-facing API.
However, much of the community got hooked on Python launchfiles due to early adoption when the frontends were incomplete.
With that in mind, and the extensive explicit use of exact filenames and `PythonLaunchDescriptionSource`, migration to these frontends is difficult for packages with downstream consumers.

Enter `launch_frontend_py` - this package provides a Python-language frontend to `launch`, with identical usage to the XML and YAML versions.
It provides the same benefits of conciseness, declarative style, while allowing launchfiles to stay in Python.


## Usage

The available actions and substitutions are identical to XML and YAML launchfiles, with one caveat:

> [!NOTE]
> Some launch Actions and their attributes use reserved Python keywords, the known cases are `for` Action and `if` attribute for conditions.
> For all cases, an underscore `_` is added at the end: `for_`, `if_`.

Here is an example launchfile with a few features:

```py
from launch_frontend_py import arg, executable, launch


def generate_launch_description():
    return launch([
        arg(name='message', default='hello world'),
        arg(name='condition', default='True'),
        executable(cmd='echo $(var message)', output='both'),
        executable(cmd='echo hello conditional', if_='$(var condition)', output='both'),
        executable(cmd='echo hello not-condition', if_='$(not $(var condition))', output='both'),
    ])
```

## Release Status

| Distro | Dev | Doc | Src | Ubuntu x64 |
|--------|-----|-----|-----|------------|
| Rolling | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Rdev__launch_frontend_py__ubuntu_noble_amd64)](https://build.ros2.org/job/Rdev__launch_frontend_py__ubuntu_noble_amd64/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Rdoc__launch_frontend_py__ubuntu_noble_amd64)](https://build.ros2.org/job/Rdoc__launch_frontend_py__ubuntu_noble_amd64/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Rsrc_uN__launch_frontend_py__ubuntu_noble__source)](https://build.ros2.org/view/Rsrc_uN/job/Rsrc_uN__launch_frontend_py__ubuntu_noble__source/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Rbin_uN64__launch_frontend_py__ubuntu_noble_amd64__binary)](https://build.ros2.org/view/Rsrc_uN/job/Rbin_uN64__launch_frontend_py__ubuntu_noble_amd64__binary/) |
| Kilted  | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Kdev__launch_frontend_py__ubuntu_noble_amd64)](https://build.ros2.org/job/Kdev__launch_frontend_py__ubuntu_noble_amd64/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Kdoc__launch_frontend_py__ubuntu_noble_amd64)](https://build.ros2.org/job/Kdoc__launch_frontend_py__ubuntu_noble_amd64/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Ksrc_uN__launch_frontend_py__ubuntu_noble__source)](https://build.ros2.org/view/Ksrc_uN/job/Ksrc_uN__launch_frontend_py__ubuntu_noble__source/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Kbin_unv8_uNv8__launch_frontend_py__ubuntu_noble_arm64__binary)](https://build.ros2.org/view/Kbin_unv8_uNv8/job/Kbin_unv8_uNv8__launch_frontend_py__ubuntu_noble_arm64__binary/) |
| Jazzy   | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Jdev__launch_frontend_py__ubuntu_noble_amd64)](https://build.ros2.org/job/Jdev__launch_frontend_py__ubuntu_noble_amd64/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Jdoc__launch_frontend_py__ubuntu_noble_amd64)](https://build.ros2.org/job/Jdoc__launch_frontend_py__ubuntu_noble_amd64/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Jsrc_uN__launch_frontend_py__ubuntu_noble__source)](https://build.ros2.org/view/Jsrc_uN/job/Jsrc_uN__launch_frontend_py__ubuntu_noble__source/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Jbin_unv8_uNv8__launch_frontend_py__ubuntu_noble_arm64__binary)](https://build.ros2.org/view/Jbin_unv8_uNv8/job/Jbin_unv8_uNv8__launch_frontend_py__ubuntu_noble_arm64__binary/) |
| Humble  | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Hdev__launch_frontend_py__ubuntu_jammy_amd64)](https://build.ros2.org/job/Hdev__launch_frontend_py__ubuntu_jammy_amd64/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Hdoc__launch_frontend_py__ubuntu_jammy_amd64)](https://build.ros2.org/job/Hdoc__launch_frontend_py__ubuntu_jammy_amd64/) |[![Build Status](https://build.ros2.org/buildStatus/icon?job=Hsrc_uJ__launch_frontend_py__ubuntu_jammy__source)](https://build.ros2.org/view/Hsrc_uJ/job/Hsrc_uJ__launch_frontend_py__ubuntu_jammy__source/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Hbin_ujv8_uJv8__launch_frontend_py__ubuntu_jammy_arm64__binary)](https://build.ros2.org/view/Hbin_ujv8_uJv8/job/Hbin_ujv8_uJv8__launch_frontend_py__ubuntu_jammy_arm64__binary/) |


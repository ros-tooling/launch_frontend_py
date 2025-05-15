from launch_py import launch, executable

def generate_launch_description():
    return launch([
        executable(cmd='echo hello launch_py world!', output='screen')
    ])

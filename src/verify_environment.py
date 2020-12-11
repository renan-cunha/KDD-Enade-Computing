import sys


REQUIRED_PYTHON_MAJOR = 3
REQUIRED_PYTHON_MINOR = 6


def verify_environment(sys) -> bool:
    system_major = sys.version_info.major
    system_minor = sys.version_info.minor
    major_requirement = system_major == REQUIRED_PYTHON_MAJOR
    minor_requirement = system_minor == REQUIRED_PYTHON_MINOR
    if not (major_requirement and minor_requirement):
        raise TypeError(f"The project requires"
                         f"Python{REQUIRED_PYTHON_MAJOR}.{REQUIRED_PYTHON_MINOR}"
                         f". Found: Python{system_major};{system_minor}")
    else:
        print(">>> Development environment passes all tests!")
        return True


if __name__ == '__main__':
    verify_environment(sys)

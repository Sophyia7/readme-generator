import platform
import pieces_os_client as client
# AI Client Configuration
configuration = client.Configuration(host="http://localhost:1000")
api_client = client.ApiClient(configuration)


def categorize_os():
    # Get detailed platform information
    platform_info = platform.platform()

    # Categorize the platform information into one of the four categories
    if 'Windows' in platform_info:
        os_info = 'WINDOWS'
    elif 'Linux' in platform_info:
        os_info = 'LINUX'
    elif 'Darwin' in platform_info:  # Darwin is the base of macOS
        os_info = 'MACOS'
    else:
        os_info = 'WEB'  # Default to WEB if the OS doesn't match others

    return os_info
def connect_api() -> client.Application:
    # Decide if it's Windows, Mac, Linux or Web
    local_os = categorize_os()


    api_instance = client.ConnectorApi(api_client)
    seeded_connector_connection = client.SeededConnectorConnection(
        application=client.SeededTrackedApplication(
            name = client.ApplicationNameEnum.OPEN_SOURCE,
            platform = local_os,
            version = "0.0.1"))
    api_response = api_instance.connect(seeded_connector_connection=seeded_connector_connection)
    application =  api_response.application
    return application


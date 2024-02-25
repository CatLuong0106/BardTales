from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from tempfile import gettempdir
import os
import sys
import subprocess
import json

def main():
    # Assuming your JSON file is named 'data.json'
    file_path = 'credentials.json'

    # Open the JSON file and load its contents
    with open(file_path, 'r') as file:
        credentials = json.load(file)

    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    # session = Session(profile_name="adminuser")
    session = Session(
        aws_access_key_id=credentials['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=credentials['AWS_SECRET_ACCESS_KEY'],
        aws_session_token=credentials['AWS_SESSION_TOKEN'],  # if using temporary credentials
        region_name=credentials['AWS_DEFAULT_REGION'],
    )
    polly = session.client("polly")

    text_file_path = "input.txt"
    with open(text_file_path, 'r', encoding='utf-8') as file: 
        content = file.read()

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Text=str(content), OutputFormat="mp3", VoiceId="Salli"
        )
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            # output = os.path.join(gettempdir(), "speech.mp3")
            output = os.path.join(".", "speech.wav")

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])

if  __name__ == "__main__": 
    main()

import sys
import requests
import json
from datetime import datetime


def main():

    if len(sys.argv) != 2:
        print("Uso: github-activity <username>")
        print("Ejemplo: github-activity kamranahmedse")
        sys.exit(1)

    username = sys.argv[1]
    api_url = f"https://api.github.com/users/{username}/events"

    try:

        response = requests.get(api_url)

        if response.status_code != 200:
            if response.status_code == 404:
                print(f"Error: Usuario '{username}' no encontrado")
            else:
                print(f"Error: API returned status code {response.status_code}")
            sys.exit(1)

        events = response.json()

        if not events:
            print(f"El usuario '{username}' no tiene actividad reciente")
            sys.exit(0)

        print(f"Actividad reciente de {username}:\n")
        for event in events[:10]:
            display_event(event)

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: No se pudo decodificar la respuesta de la API")
        sys.exit(1)


def display_event(event):

    event_type = event['type']
    repo_name = event['repo']['name']

    messages = {
        'PushEvent': f"Pushed {event['payload'].get('size', 'some')} commits to {repo_name}",
        'IssuesEvent': f"{event['payload']['action'].capitalize()} an issue in {repo_name}",
        'IssueCommentEvent': f"Commented on an issue in {repo_name}",
        'WatchEvent': f"Starred {repo_name}",
        'ForkEvent': f"Forked {repo_name}",
        'PullRequestEvent': f"{event['payload']['action'].capitalize()} a pull request in {repo_name}",
        'CreateEvent': f"Created a {event['payload']['ref_type']} in {repo_name}",
        'DeleteEvent': f"Deleted a {event['payload']['ref_type']} in {repo_name}",
        'ReleaseEvent': f"Released {event['payload']['release']['tag_name']} in {repo_name}"
    }

    message = messages.get(event_type, f"{event_type} in {repo_name}")

    if 'created_at' in event:
        timestamp = format_timestamp(event['created_at'])
        print(f"- {message} ({timestamp})")
    else:
        print(f"- {message}")


def format_timestamp(iso_timestamp):

    try:
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return iso_timestamp


if __name__ == "__main__":
    main()
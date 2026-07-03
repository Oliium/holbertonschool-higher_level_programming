#!/usr/bin/python3
"""Generate personalized invitation files from a template."""


def generate_invitations(template, attendees):
    """Generate invitation files from a template and a list of attendees.

    Args:
        template (str): The template string with placeholders.
        attendees (list): A list of dictionaries with attendee data.
    """
    # Validate input types
    if not isinstance(template, str):
        print("Invalid input: template must be a string, got "
              "{}".format(type(template).__name__))
        return
    if (not isinstance(attendees, list) or
            not all(isinstance(a, dict) for a in attendees)):
        print("Invalid input: attendees must be a list of dictionaries")
        return

    # Handle empty inputs
    if template == "":
        print("Template is empty, no output files generated.")
        return
    if len(attendees) == 0:
        print("No data provided, no output files generated.")
        return

    placeholders = ["name", "event_title", "event_date", "event_location"]

    for index, attendee in enumerate(attendees, start=1):
        content = template
        for key in placeholders:
            value = attendee.get(key)
            if value is None:
                value = "N/A"
            content = content.replace("{" + key + "}", str(value))

        output_file = "output_{}.txt".format(index)
        with open(output_file, "w") as file:
            file.write(content)

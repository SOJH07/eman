import core_logic

def generate_prayer_list_html(daily_schedule, surah_data):
    """Generates the HTML list items from the daily schedule data."""
    # Create a quick lookup map from surah name to surah id
    surah_name_to_id = {s['name']: s['id'] for s in surah_data}

    html = ""
    for prayer, surah_name in daily_schedule.items():
        surah_id = surah_name_to_id.get(surah_name)
        if surah_id:
            # Link to the specific surah page
            link = f"surah_{surah_id}.html"
            html += f"""
                <li class="prayer-item">
                    <span class="prayer-name">{prayer}</span>
                    <a href="{link}" class="surah-link">
                        <span class="arrow">&lt;</span>
                        <span>{surah_name}</span>
                    </a>
                </li>
            """
    return html

def create_surah_pages(surahs, template_html):
    """Generates an individual HTML page for each surah."""
    print("\n--- Generating individual Surah pages ---")
    for surah in surahs:
        surah_id = surah['id']
        surah_name = surah['name']
        # Format the text with verses
        verses = surah['text'].split('\n')
        surah_text_html = f'<p class="bismillah">{verses[0]}</p>'
        for verse in verses[1:]:
            surah_text_html += f'<p class="verse">{verse}</p>'

        # Replace placeholders
        page_html = template_html.replace("<!-- SURAH_NAME_PLACEHOLDER -->", surah_name)
        page_html = page_html.replace("<!-- SURAH_TEXT_PLACEHOLDER -->", surah_text_html)
        # Point the back button to the main index page
        page_html = page_html.replace('href="main_screen.html"', 'href="index.html"')


        filename = f"surah_{surah_id}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  -> Created {filename}")

def main():
    """Main function to integrate logic with UI and generate the final HTML."""
    print("--- Starting Integration ---")

    # 1. Get the data from the backend logic
    surahs = core_logic.load_surahs()
    weekly_schedule = core_logic.generate_weekly_schedule(surahs)

    # We'll use Day 1's schedule for this simulation
    day_1_schedule = weekly_schedule.get("Day 1", {})

    if not day_1_schedule:
        print("Could not get schedule for Day 1. Aborting.")
        return

    print("\n--- Dynamically generating main page HTML content ---")
    # 2. Generate the dynamic part of the HTML for the main page
    prayer_list_html = generate_prayer_list_html(day_1_schedule, surahs)

    # 3. Read the UI templates
    try:
        with open("main_screen.html", "r", encoding="utf-8") as f:
            main_template_html = f.read()
        with open("surah_template.html", "r", encoding="utf-8") as f:
            surah_template_html = f.read()
    except FileNotFoundError as e:
        print(f"Error: Template file not found. {e}")
        return

    # 4. Inject the dynamic HTML into the main page template
    final_main_html = main_template_html.replace("<!-- PRAYER_LIST_PLACEHOLDER -->", prayer_list_html)

    # 5. Save the final rendered main page
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_main_html)
    print("  -> Successfully created index.html with dynamic data.")

    # 6. Generate the individual surah pages
    create_surah_pages(surahs, surah_template_html)

    print("\n--- Integration Complete ---")

if __name__ == "__main__":
    main()

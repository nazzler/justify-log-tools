JUSTIFY = F"""
        query get_reports_data {{
            reportData {{
                reports (
                    guildName: "Justify",
                    guildServerSlug: "Silvermoon",
                    guildServerRegion: "EU",
                    startTime: 1598918400
                    page: 1,
                    zoneID: 24) {{
                    total
                    has_more_pages
                    current_page
                    data {{
                        code
                    }}
                }}
            }}
        }}
        """

TOP100X = \
"""
{
  publisherCommissions(forPublishers: ["999"]) {
    records
  }
}
"""

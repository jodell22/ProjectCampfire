# Project Campfire 🔥

Project Campfire is a Discord-integrated Dungeons & Dragons companion bot designed to bring a seamless, multi-channel, story-driven experience to your campaigns. Built with GPT-4 integration, it splits gameplay into multiple channels (e.g. DM-only, players/world, out-of-character) to help manage narrative flow and world-building immersion.

The bot supports:
- Dynamic narrative responses powered by AI
- Player sheet integration and persistent character memory
- Channel-specific intelligence (DM secrecy vs public story)
- Modular deployment on Ubuntu using Ansible

Whether you're running an epic saga or just a one-shot with friends, Campfire makes it feel like you're huddled around the real thing.

*Let the stories burn bright.*

===============================

🔐 Discord Bot Permissions
To function correctly across all channels in the Project Campfire server, the bot requires the following permissions:

Required Permissions
These are necessary for basic functionality:

- Read Messages/View Channels – To see messages in channels it has access to
- Send Messages – To respond to prompts and interact with users
- Embed Links – To format messages with rich content
- Attach Files – For sending logs, images, or exports
- Read Message History – So it can reply to previous messages intelligently
- Use Slash Commands – For modern interactions and commands

Optional (but recommended) Permissions
These enhance functionality but aren’t required:

- Manage Messages – Allows bot to delete or edit its own messages
- Add Reactions – For reaction-based input or voting
- Manage Webhooks – If you're integrating dynamic notifications or storytelling triggers
- Manage Roles – If the bot assigns character roles or world status


===============================
Install command:
curl -sSL https://raw.githubusercontent.com/jodell22/ProjectCampfire/main/scripts/install.sh | bash


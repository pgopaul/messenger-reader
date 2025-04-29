import json
import os
from datetime import datetime

# ===== SETTINGS =====
folder_path = 'input'                   # Folder containing message_1.json, message_2.json, etc.
your_name = 'insert your facebook username here'           # Your Facebook name

# ===== LOAD AND COMBINE MESSAGES =====
all_messages = []
participants = set()

for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.json'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
            participants.update(p['name'] for p in data['participants'])
            all_messages.extend(data['messages'])

all_messages.reverse()  # Facebook stores newest first

# ===== CREATE HTML =====
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Facebook Messenger Chat</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            background-color: var(--bg);
            color: var(--text);
            transition: background-color 0.3s, color 0.3s;
        }}

        :root {{
            --bg: #f0f2f5;
            --text: #000;
            --bubble-me: #0084ff;
            --bubble-other: #e4e6eb;
        }}

        body.dark {{
            --bg: #18191a;
            --text: #e4e6eb;
            --bubble-me: #3a3b3c;
            --bubble-other: #242526;
        }}

        .chat-container {{
            width: 100%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
        }}

        .message {{
            max-width: 90%;
            margin: 10px;
            padding: 10px 15px;
            border-radius: 20px;
            word-wrap: break-word;
            clear: both;
        }}

        .me {{
            background-color: var(--bubble-me);
            color: white;
            margin-left: auto;
            text-align: right;
            float: right;
        }}

        .other {{
            background-color: var(--bubble-other);
            color: black;
            margin-right: auto;
            text-align: left;
            float: left;
        }}

        body.dark .other {{
            color: white;
        }}

        .timestamp {{
            font-size: 0.8em;
            color: gray;
            margin-top: 5px;
        }}

        .toggle {{
            position: fixed;
            top: 10px;
            right: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="toggle">
        <label>
            <input type="checkbox" id="darkToggle" /> Dark Mode
        </label>
    </div>
    <div class="chat-container">
        <h2>Chat between {', '.join(participants)}</h2>
'''

# ===== ADD MESSAGES =====
for msg in all_messages:
    sender = msg.get('sender_name', 'Unknown')
    timestamp_ms = msg.get('timestamp_ms')

    # Fix corrupted emoji content
    raw_content = msg.get('content', '')
    try:
        content = raw_content.encode('latin1').decode('utf-8')
    except:
        content = raw_content

    if content:
        content = content.replace('\n', '<br>')

    if timestamp_ms:
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000.0).strftime('%Y-%m-%d %H:%M')
    else:
        timestamp = 'Unknown time'

    css_class = 'me' if sender == your_name else 'other'

    html_content += f'''
        <div class="message {css_class}">
            <div><strong>{sender}</strong></div>
            <div>{content}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
    '''

# ===== END HTML =====
html_content += '''
    </div>
    <script>
        const toggle = document.getElementById('darkToggle');
        toggle.addEventListener('change', () => {
            document.body.classList.toggle('dark', toggle.checked);
        });
    </script>
</body>
</html>
'''

# ===== SAVE HTML =====
output_file = 'chat.html'
with open(output_file, 'w', encoding='utf-8-sig') as f:
    f.write(html_content)

print(f"✅ Done! Open {output_file} in your browser to view the chat with dark mode support.")

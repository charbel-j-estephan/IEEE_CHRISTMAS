import tkinter as tk
from tkinter import colorchooser, messagebox
import os
import webbrowser
import json
import subprocess
import datetime

def create_html_file(message, color="#ff3366", delay=5, filename="winter_led.html"):
    """Create the complete HTML file with LED message"""

    # Ensure the 'docs' directory exists
    docs_dir = "docs"
    os.makedirs(docs_dir, exist_ok=True)
    filepath = os.path.join(docs_dir, filename)

    # Use JSON to properly escape the message for embedding in JavaScript
    escaped_message = json.dumps(message)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Winter Landscape with LED Message</title>
<style>
html, body {{
  margin: 0;
  padding: 0;
  overflow: hidden;
}}

#led-message {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 15px; /* Added gap for spacing */
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  animation: fadeIn 2s ease-in {delay}s forwards;
  background: rgba(0, 0, 0, 0.7);
  padding: clamp(10px, 1.5vw, 20px);
  border-radius: 10px;
  border: 2px solid {color};
  box-shadow:
    0 0 20px rgba(255, 51, 102, 0.5),
    inset 0 0 20px rgba(255, 51, 102, 0.2);
  overflow: auto;
  z-index: 1000;
}}

#ascii-art {{
  font-family: 'Courier New', monospace;
  font-size: clamp(24px, 4vw, 48px);
  color: {color};
  text-shadow:
    0 0 10px {color},
    0 0 20px {color},
    0 0 30px {color},
    0 0 40px {color};
  white-space: pre;
  margin: 0;
  padding: 0;
  text-align: left;
}}

#ieee-sub-message {{
  font-family: 'Arial', sans-serif;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  white-space: nowrap;
}}

@keyframes fadeIn {{
  to {{ opacity: 1; }}
}}

@keyframes blink {{
  0%, 100% {{ opacity: 1; }}
  50% {{ opacity: 0.7; }}
}}

.blink {{
  animation: blink 2s infinite;
}}

</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="led-message" class="blink">
    <pre id="ascii-art"></pre>
    <div id="ieee-sub-message">🎄 Merry Christmas from IEEE NDU 🎄</div>
</div>

<script>
const c = document.querySelector("#c");
const ctx = c.getContext("2d");
const dpr = 0.5;
c.width = window.innerWidth * dpr;
c.height = window.innerHeight * dpr;
c.style.width = "100vw";
c.style.height = "100vh";
c.style.imageRendering = "pixelated";

const palette = [
  "#65dcf3",
  "hsl(204deg 67% 44%)",
  "#4ca7df",
  "#367cb1",
  "#286097"
];

const lights = [
  "hsl(323deg, 78%, 75%)",
  "hsl(42deg, 61%, 75%)",
  "hsl(143deg, 61%, 75%)"
];

const windows = [
  ["#286097", "#1f4c7d"],
  ["#286097", "#1f4c7d"],
  ["#286097", "#1f4c7d"],
  ["#286097", "#1f4c7d"],
  ["#e087a7", "#c172ab"],
  ["#5fb7e7", "#4aa2d4"],
  ["#7ad2a1", "#4ea695"]
];

const bgGradient = ctx.createLinearGradient(0, 0, 0, c.height);
bgGradient.addColorStop(0, palette[1]);
bgGradient.addColorStop(1, palette[1]);

const getScreenCoords = (left, x, y) => {{
  return [x, Math.floor(left ? y + (x / c.width) * height : y + (1 - x / c.width) * height)];
}};

const sectionHeight = 600 * dpr;
const width = c.width;
const height = 300 * dpr;
const levels = 7;
const levelHeight = height / (levels + 1);
const levelWidth = levelHeight * (3.6 / 3.0);
const windowHeight = levelHeight * (1.5 / 3.0);
const windowWidth = windowHeight * (2.4 / 1.5);
const windowLeftPadding = (levelWidth - windowWidth) / 2;
const windowTopPadding = (levelHeight - windowHeight) / 2;
const colls = Math.ceil(c.width / levelWidth);

const drawGradientRhombus = (left, x, y, width, height, colorFrom, colorTo) => {{
  const ratio = height / width / (Math.PI * 2);
  const gradientCoords = [
    ...getScreenCoords(left, x + width * (left ? 0.5 + ratio : 0.5 - ratio), y),
    ...getScreenCoords(left, x + width * (left ? 0.5 - ratio : 0.5 + ratio), y + height)
  ];
  const houseLeftGradient = ctx.createLinearGradient(...gradientCoords);
  houseLeftGradient.addColorStop(0, colorFrom);
  houseLeftGradient.addColorStop(1, colorTo);
  ctx.fillStyle = houseLeftGradient;
  ctx.beginPath();
  ctx.moveTo(...getScreenCoords(left, x, y));
  ctx.lineTo(...getScreenCoords(left, x, y + height));
  ctx.lineTo(...getScreenCoords(left, x + width, y + height));
  ctx.lineTo(...getScreenCoords(left, x + width, y));
  ctx.closePath();
  ctx.fill();
}};

const drawWindow = (left, x, y, colors) => {{
  ctx.strokeStyle = palette[3];
  drawGradientRhombus(left, x, y, windowWidth, windowHeight, ...colors);
  ctx.stroke();
  ctx.strokeStyle = palette[3];
  ctx.beginPath();
  ctx.moveTo(...getScreenCoords(left, x + windowWidth * 0.3, y));
  ctx.lineTo(...getScreenCoords(left, x + windowWidth * 0.3, y + windowHeight));
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(...getScreenCoords(left, x + windowWidth * 0.7, y));
  ctx.lineTo(...getScreenCoords(left, x + windowWidth * 0.7, y + windowHeight));
  ctx.stroke();
}};

const drawPadik = (left, x, y, colors) => {{
  drawGradientRhombus(left, x - windowLeftPadding, y - windowTopPadding, levelWidth, levelHeight, palette[3], palette[3]);
  drawGradientRhombus(left, x, y, windowWidth, windowHeight, palette[4], palette[4]);
  ctx.strokeStyle = palette[3];
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(...getScreenCoords(left, x + windowWidth * 0.3, y));
  ctx.lineTo(...getScreenCoords(left, x + windowWidth * 0.3, y + windowHeight));
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(...getScreenCoords(left, x + windowWidth * 0.7, y));
  ctx.lineTo(...getScreenCoords(left, x + windowWidth * 0.7, y + windowHeight));
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(...getScreenCoords(left, x, y + windowHeight * 0.5));
  ctx.lineTo(...getScreenCoords(left, x + windowWidth, y + windowHeight * 0.5));
  ctx.stroke();
  ctx.lineWidth = 1;
}};

const distance = (x1, y1, x2, y2) => {{
  return Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
}};

const generateTreeTexture = () => {{
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = canvas.height = 300 * dpr;
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  for (let y = 0; y < canvas.height; y++) {{
    for (let x = 0; x < canvas.width; x++) {{
      if (distance(x, y, cx, cy) < cx * (0.7 + Math.random() * 0.3)) {{
        const w = Math.random();
        const h = 1 - y / canvas.height;
        ctx.fillStyle = `hsl(206deg, 69%, ${{30 + w * 70 * h}}%)`;
        ctx.fillRect(x, y, 1, 1);
      }}
    }}
  }}
  return canvas;
}};

const threeCanvas = generateTreeTexture();

const generateChristmasTreeTexture = () => {{
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = 200 * dpr;
  canvas.height = 300 * dpr;

  function drawTriangle(x1, y1, x2, y2, x3, y3, color) {{
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1 + (x2 - x1) * 0.5, y1 * 1.15);
    ctx.lineTo(x2, y2);
    ctx.lineTo(x3, y3);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
  }}

  const baseX = canvas.width / 2;
  const baseY = canvas.height;
  const width = canvas.width;
  const height = canvas.height;
  const levels = 5;

  for (let i = 0; i < levels; i++) {{
    const levelHeight = height / levels;
    const levelWidth = width - (i * width) / levels;
    const topX = baseX;
    const topY = baseY - (i + 1) * levelHeight;
    const leftX = baseX - levelWidth / 2;
    const rightX = baseX + levelWidth / 2;
    const bottomY = baseY - i * levelHeight;

    const darkColor = `hsl(204deg 67% ${{24 + i * 5}}%)`;
    drawTriangle(leftX, bottomY + 2, rightX, bottomY + 2, topX, topY, darkColor);

    const snowColor = `hsl(204deg 67% ${{50 + i * 5}}%)`;
    drawTriangle(leftX, bottomY - 2, rightX, bottomY - 2, topX, topY, snowColor);
  }}
  return canvas;
}};

const christmassThreeCanvas = generateChristmasTreeTexture();

const drawTreesLine = (left, x, y) => {{
  const treesCount = 5;
  for (let t = -1; t < treesCount; t++) {{
    const [tx, ty] = getScreenCoords(left, x + t * (200 * dpr), left ? y + height : y + height - 20);
    ctx.drawImage(threeCanvas, tx, ty + Math.sin(tx * 10) * 10 - 10);
  }}
}};

const asciiElement = document.querySelector('#ascii-art');
const rawMessage = {escaped_message};

// Split into lines and pad each to the max width to center the ascii art
const lines = rawMessage.split('\n');
const maxLen = Math.max(...lines.map(line => line.length));
const padded = lines.map(line => {{
  const totalPadding = maxLen - line.length;
  const leftPad = ' '.repeat(Math.floor(totalPadding / 2));
  return leftPad + line;
}});

asciiElement.textContent = padded.join('\n');

// Mobile specific adjustments
if (window.innerWidth <= 768) {{
    document.querySelector('#ascii-art').style.fontSize = '5vw';
}}

const animate = (time) => {{
  requestAnimationFrame(animate);
  const count = 3;
  const sy = time / 100 / dpr;
  ctx.resetTransform();
  ctx.fillStyle = bgGradient;
  ctx.fillRect(0, 0, c.width, c.height);
  ctx.translate(0, sy % (sectionHeight * 2));

  for (let i = -2; i < count * 2; i++) {{
    const y = i * sectionHeight;
    const x = (c.width - width) / 2;

    drawTreesLine(i % 2, x, y - height - 25);
    drawGradientRhombus(i % 2, x, y - height / 3, c.width, height / 3, palette[2], palette[0]);
    drawGradientRhombus(i % 2, x, y, c.width, height, palette[2], palette[3]);

    for (let row = 0.5; row < levels; row++) {{
      for (let col = 0; col < colls; col++) {{
        const random = () => {{
          return Math.abs(Math.sin(i) + Math.cos(row) + Math.sin(col)) % 1;
        }};

        const colors = windows[Math.floor(random() * windows.length) % windows.length];
        const left = col * levelWidth + windowLeftPadding + x;
        const top = row * levelHeight + windowTopPadding + y;

        if (i % 2 === 0 && col % 6 < 2) {{
          drawPadik(i % 2, left, top, ["red", "red"]);
        }} else {{
          drawWindow(i % 2, left, top, colors);
        }}
      }}
    }}

    ctx.strokeStyle = palette[4];
    for (let col = 0; col < colls; col++) {{
      ctx.beginPath();
      ctx.moveTo(...getScreenCoords(i % 2, col * levelWidth + x, y));
      ctx.lineTo(...getScreenCoords(i % 2, col * levelWidth + x, y + height));
      ctx.stroke();
    }}

    ctx.beginPath();
    ctx.moveTo(...getScreenCoords(i % 2, 0, y));
    ctx.lineTo(...getScreenCoords(i % 2, c.width, y));
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(...getScreenCoords(i % 2, 0, y + 1));
    ctx.lineTo(...getScreenCoords(i % 2, c.width, y + 1));
    ctx.stroke();

    for (let row = 0.5; row < levels + 1; row++) {{
      ctx.beginPath();
      ctx.moveTo(...getScreenCoords(i % 2, 0, row * levelHeight + y));
      ctx.lineTo(...getScreenCoords(i % 2, c.width, row * levelHeight + y));
      ctx.stroke();
    }}

    const iciclesCount = c.width / 3;
    ctx.fillStyle = palette[0];
    ctx.beginPath();
    ctx.moveTo(...getScreenCoords(i % 2, x, y - 1));
    for (let j = 0; j < iciclesCount; j++) {{
      ctx.lineTo(...getScreenCoords(i % 2, x + j * 3, y + 10 * Math.abs(Math.sin(j) * Math.sin(j / 10))));
      ctx.lineTo(...getScreenCoords(i % 2, x + j * 3 + 3, y));
    }}
    ctx.fill();

    drawTreesLine(i % 2, x, y);

    const ct_x = i % 2 ? x + 5 : x + width - 55;
    const ct_y = y + 100;
    const ct_c = ct_x + (christmassThreeCanvas.width / 2);
    ctx.drawImage(christmassThreeCanvas, ct_x, ct_y);

    ctx.strokeStyle = lights[Math.floor(time / 1000) % lights.length];
    ctx.beginPath();
    ctx.moveTo(ct_c, ct_y);
    ctx.lineTo(ct_c - 5, ct_y + 7);
    ctx.lineTo(ct_c, ct_y + 14);
    ctx.lineTo(ct_c + 5, ct_y + 15);
    ctx.lineTo(ct_c, ct_y + 22);
    ctx.lineTo(ct_c - 8, ct_y + 25);
    ctx.lineTo(ct_c, ct_y + 32);
    ctx.lineTo(ct_c + 8, ct_y + 35);
    ctx.lineTo(ct_c, ct_y + 43);
    ctx.lineTo(ct_c - 14, ct_y + 45);
    ctx.lineTo(ct_c, ct_y + 53);
    ctx.lineTo(ct_c + 14, ct_y + 55);
    ctx.lineTo(ct_c, ct_y + 62);
    ctx.lineTo(ct_c - 18, ct_y + 56);
    ctx.stroke();
  }}

  ctx.resetTransform();
  const snowCount = 100;
  ctx.fillStyle = "white";
  for (let i = 0; i < snowCount; i++) {{
    const bx = (i % 10) / 10;
    const by = Math.floor(i / 10) / 10;
    const sx = 0.1 * Math.sin(by * 100) + 0.05 * Math.sin(by * 100) * Math.sin(time / 600);
    const sy = 0.1 * Math.sin(bx * 100) + time / 6000 / Math.abs(Math.sin(bx * 200));
    const x = (bx + sx) * c.width;
    const y = ((by + sy) * c.height) % c.height;
    ctx.fillRect(x, y, 2, 2);
  }}
}};

animate(0);
</script>
</body>
</html>'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return filepath


class LEDGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎄 ASCII LED Message Generator")
        self.root.geometry("700x650")
        self.root.resizable(False, False)

        self.color = "#ff3366"
        self.created_file = None

        self.create_widgets()

    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="🎄 ASCII LED Message Generator",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Your ASCII Art Message:", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        tk.Label(main_frame, text="(Enter any ASCII art)", font=("Arial", 9), fg="gray").pack(anchor=tk.W)

        self.message_text = tk.Text(main_frame, height=10, font=("Courier New", 11), wrap=tk.WORD)
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=(5, 15))
        self.message_text.insert("1.0", "HAPPY HOLIDAYS")

        settings_frame = tk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, pady=(0, 15))

        left_col = tk.Frame(settings_frame)
        left_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        color_frame = tk.Frame(left_col)
        color_frame.pack(fill=tk.X, pady=5)
        tk.Label(color_frame, text="LED Color:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.color_btn = tk.Button(
            color_frame,
            text="    ",
            bg=self.color,
            width=5,
            command=self.pick_color
        )
        self.color_btn.pack(side=tk.LEFT, padx=10)
        self.color_label = tk.Label(color_frame, text=self.color, font=("Courier New", 9))
        self.color_label.pack(side=tk.LEFT)

        delay_frame = tk.Frame(left_col)
        delay_frame.pack(fill=tk.X, pady=5)
        tk.Label(delay_frame, text="Delay (seconds):", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.delay_var = tk.IntVar(value=5)
        self.delay_slider = tk.Scale(
            delay_frame,
            from_=0,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.delay_var,
            length=200
        )
        self.delay_slider.pack(side=tk.LEFT, padx=10)

        right_col = tk.Frame(settings_frame)
        right_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))

        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))

        action_frame = tk.Frame(button_frame)
        action_frame.pack(side=tk.RIGHT)

        self.generate_btn = tk.Button(
            action_frame,
            text="🚀 Generate HTML",
            command=self.generate_html,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.open_btn = tk.Button(
            action_frame,
            text="🌐 Open in Browser",
            command=self.open_in_browser,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.open_btn.pack(side=tk.LEFT, padx=5)

        self.deploy_btn = tk.Button(
            action_frame,
            text="🚀 Deploy to GitHub",
            command=self.deploy_to_github,
            bg="#4a4a4a",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.deploy_btn.pack(side=tk.LEFT, padx=5)

    def deploy_to_github(self):
        # First, generate the file.
        created_file_path = self.generate_html()

        if not created_file_path:
            # The generate_html method already shows an error, so we can just return.
            return

        try:
            # Add the specific file to git
            subprocess.run(["git", "add", created_file_path], check=True)

            # Commit the changes
            commit_message = f"Deploy: {os.path.basename(created_file_path)}"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)

            # Push the changes
            subprocess.run(["git", "push"], check=True)

            # Get repo URL to show the user
            repo_url_proc = subprocess.run(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True, check=True)
            repo_url = repo_url_proc.stdout.strip()
            
            # Construct the GitHub Pages URL
            if repo_url.endswith('.git'):
                repo_url = repo_url[:-4]
            if repo_url.startswith('https://'):
                username, repo_name = repo_url.split('/')[-2:]
                pages_url = f"https://{username}.github.io/{repo_name}/{os.path.basename(created_file_path)}"
                
                # Copy URL to clipboard
                self.root.clipboard_clear()
                self.root.clipboard_append(pages_url)
                
                messagebox.showinfo("Success! 🎉", f"Deployment successful!\n\nURL: {pages_url}\n(Copied to clipboard!)")
            else:
                messagebox.showinfo("Success! 🎉", "Deployment to GitHub Pages successful!")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Deployment Error", f"Failed to deploy to GitHub:\n{e.stderr or e.stdout or str(e)}")
        except FileNotFoundError:
            messagebox.showerror("Deployment Error", "Git command not found. Make sure Git is installed and in your system's PATH.")

    def pick_color(self):
        color = colorchooser.askcolor(initialcolor=self.color, title="Choose LED Color")
        if color[1]:
            self.color = color[1]
            self.color_btn.config(bg=self.color)
            self.color_label.config(text=self.color)

    def generate_html(self):
        message = self.message_text.get("1.0", tk.END).strip()

        if not message:
            messagebox.showwarning("Empty Message", "Please enter a message!")
            return None # Return None on failure

        delay = self.delay_var.get()
        
        filename = f"message-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.html"

        try:
            self.created_file = create_html_file(message, self.color, delay, filename)

            messagebox.showinfo(
                "Success! 🎉",
                f"File created successfully!\n\n📄 {filename}\n📍 {os.path.abspath(self.created_file)}"
            )

            self.open_btn.config(state=tk.NORMAL)
            return self.created_file # Return the path of the created file

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create file:\n{str(e)}")
            return None # Return None on failure

    def open_in_browser(self):
        if self.created_file and os.path.exists(self.created_file):
            webbrowser.open('file://' + os.path.abspath(self.created_file))
        else:
            messagebox.showwarning("No File", "Please generate the HTML file first!")


def main():
    root = tk.Tk()
    app = LEDGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
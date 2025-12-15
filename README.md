<!DOCTYPE html>
<html lang="en">
<body>

<h1>🧙 AI Invisibility Cloak (QR Controlled)</h1>

<p>
Turn yourself invisible in real time using computer vision and a red cloak.
This project uses <strong>OpenCV</strong> and <strong>Python</strong> to detect a red cloth,
remove it from the camera feed, and replace it with a captured background —
creating a <em>Harry Potter–style invisibility effect</em>.
</p>

<p>
Instead of buttons or a GUI, the cloak is controlled using <strong>QR codes</strong>.
</p>

<span class="badge">OpenCV</span>
<span class="badge">Computer Vision</span>
<span class="badge">Python</span>
<span class="badge">QR Control</span>

<h2>✨ Features</h2>
<ul>
    <li>⚡ Real-time invisibility effect (typically 30+ FPS)</li>
    <li>🎨 HSV-based color segmentation for reliable red-cloak detection</li>
    <li>📱 QR code control:
        <ul>
            <li><code>CLOAK_ON</code> / <code>INVISIBLE</code> → Activate cloak</li>
            <li><code>CLOAK_OFF</code> / <code>VISIBLE</code> → Deactivate cloak</li>
            <li><code>TOGGLE</code> → Switch state</li>
        </ul>
    </li>
    <li>🖼️ Static or dynamic background replacement</li>
    <li>📊 On-screen HUD with live FPS counter and cloak status</li>
    <li>⌨️ Keyboard fallbacks (<code>C</code> to toggle, <code>ESC</code> to quit)</li>
</ul>

<h2>⚙️ How It Works</h2>

<h3>1. Background Capture</h3>
<p>
At startup, the camera records several frames while you are not in front of it.
These frames are combined into a clean background image.
</p>

<h3>2. Color-Based Cloak Detection</h3>
<ul>
    <li>Each frame is flipped horizontally for a mirror-like view</li>
    <li>Blurred slightly to reduce noise</li>
    <li>Converted from BGR to HSV color space</li>
    <li>Two red hue ranges (around 0° and 180°) create a cloak mask</li>
</ul>

<h3>3. Mask Refinement</h3>
<p>Morphological operations are applied to:</p>
<ul>
    <li>Remove noise</li>
    <li>Fill gaps</li>
    <li>Smooth cloak edges</li>
</ul>

<h3>4. Compositing</h3>
<p>
Pixels detected as cloak are replaced with pixels from the stored background.
All other pixels come from the live camera feed, producing the invisibility illusion.
</p>

<h3>5. QR Code Control</h3>
<p>
Each frame is scanned for QR codes. Decoded commands update the cloak state
with a cooldown to prevent repeated triggers.
</p>

<h2>📦 Requirements</h2>
<ul>
    <li>Python 3.8+</li>
    <li>Webcam</li>
    <li>Red cloth or fabric</li>
    <li>Python packages:</li>
</ul>

<pre><code>pip install opencv-python numpy pyzbar</code></pre>

<h2>🚀 Installation & Usage</h2>

<h3>Clone the Repository</h3>
<pre><code>git clone https://github.com/&lt;your-username&gt;/qr-invisibility-cloak.git
cd qr-invisibility-cloak</code></pre>

<h3>Install Dependencies</h3>
<pre><code>pip install opencv-python numpy pyzbar</code></pre>

<h3>Generate QR Codes (Optional)</h3>
<pre><code>python QRCodeGen.py</code></pre>
<p>Or use the pre-generated QR codes in the <code>QR's Generated</code> folder.</p>

<h3>Run the Invisibility Cloak</h3>
<pre><code>python InvisibilityCloak.py</code></pre>

<div class="note">
<strong>Setup Instructions:</strong>
<ul>
    <li>Remove the red cloth from the camera view</li>
    <li>Wait for background capture (~3 seconds)</li>
    <li>Put on your red cloak</li>
    <li>Show QR codes to control the effect</li>
</ul>
</div>

<h2>🎮 Controls</h2>

<h3>QR Codes</h3>
<ul>
    <li><code>cloak_on.png</code> → Activate cloak</li>
    <li><code>cloak_off.png</code> → Deactivate cloak</li>
    <li><code>toggle.png</code> → Toggle state</li>
</ul>

<h3>Keyboard</h3>
<ul>
    <li><code>C</code> → Toggle cloak</li>
    <li><code>ESC</code> → Exit program</li>
</ul>

<h2>📁 Project Structure</h2>
<pre><code>.
├── QR's Generated/
│   ├── cloak_off.png
│   ├── cloak_on.png
│   └── toggle.png
├── InvisibilityCloak.py
├── QRCodeGen.py
└── README.md
</code></pre>

<h2>🎛️ Tuning the Effect</h2>
<p>Adjust HSV values in <code>InvisibilityCloak.py</code> if detection is noisy:</p>

<pre><code>lower_red1 = np.array([0, 100, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 50])
upper_red2 = np.array([180, 255, 255])</code></pre>

<ul>
    <li>Use uniform lighting</li>
    <li>Avoid pink or orange fabrics</li>
    <li>Tune morphological iterations</li>
    <li>Maintain moderate camera distance</li>
</ul>

<h2>🧠 Technical Details</h2>
<ul>
    <li><strong>Color Detection:</strong> HSV segmentation</li>
    <li><strong>Image Processing:</strong> Morphological operations</li>
    <li><strong>QR Detection:</strong> pyzbar</li>
    <li><strong>Performance:</strong> 30+ FPS optimized pipeline</li>
    <li><strong>Background:</strong> Median-based capture</li>
</ul>

<h2>🚧 Possible Extensions</h2>
<ul>
    <li>🎮 Gesture-based control</li>
    <li>👥 Multi-person or multi-color cloaks</li>
    <li>🎥 OBS virtual camera support</li>
    <li>🖱️ GUI for live HSV tuning</li>
    <li>📦 Standalone app with PyInstaller</li>
    <li>🌍 Custom background images or videos</li>
</ul>

<h2>🤝 Contributing</h2>
<p>Fork the project and submit pull requests for improvements.</p>


<footer>
Built with OpenCV & Python<br> QR-Controlled Interaction<br><br>
<strong>Made by Justin Thomas</strong><br>

</body>
</html>

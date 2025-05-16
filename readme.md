# WEBAPP-EYESPHERE

# 🏥 Dynamic Snellen Chart Web App

This web app dynamically generates a **Snellen eye chart** based on the physical size (in inches) of your screen and your screen resolution. It allows you to:

- Render a Snellen chart scaled correctly in **pixel size** according to screen dimensions.
- Highlight a particular line number and fetch predicted diopters via a form.
- Generate a **PDF** version of the chart with the highlighted line.
- Enter fullscreen for better test display.
- Toggle **dark/light theme**.
- Auto-detect your **screen resolution** to calculate correct character sizes.

---

## 🚀 Features

- ✅ Dynamic scaling based on physical screen diagonal
- ✅ Uses screen resolution (`window.screen.width`, `height`) to compute PPI
- ✅ Calculates pixel height of each Snellen line using **logMAR** formula
- ✅ Fullscreen & PDF download support
- ✅ Server interaction to POST selected line for diopter prediction
- ✅ Theme toggle & dark mode support

---

## 🛠 How It Works

### 📐 Step 1: User Input for Diagonal Size

The user inputs the **physical screen diagonal (in inches)**.

```html
<input type="number" id="diagonal" name="diagonal" step="0.1" required>

🖥 Step 2: Automatically Reading Screen Resolution
The script detects the screen resolution using built-in browser properties:

`javascript`

`const width_px = window.screen.width;`
`const height_px = window.screen.height;`
These give the horizontal and vertical resolution of the screen in pixels (e.g., 1920×1080).

📏 Step 3: Calculating Screen PPI (Pixels Per Inch)
With the screen resolution and the user-provided diagonal size, the script calculates PPI (Pixels Per Inch) using the formula:

`javascript`

const diagonal_px = Math.sqrt(width_px ** 2 + height_px ** 2);
const ppi = diagonal_px / diagonal_inch;
This determines how many pixels fit into one physical inch on your screen, which is crucial for scaling the Snellen chart correctly.

📐 Step 4: Calculating Pixel Sizes for Each Snellen Line
The Snellen chart lines are sized using the logMAR (logarithm of the Minimum Angle of Resolution) principle.

The app uses a base height of characters at a 3-meter distance:

javascript

const base_height_m = 0.00435;
Then for each line, it calculates the required height using the logMAR formula:

javascript

const logmar = (10 - i) * 0.1;
const height_m = base_height_m * Math.pow(10, logmar);
const height_mm = height_m * 1000;
const pixel_size = height_mm * (ppi / 25.4); // convert mm to px
Why use 25.4?
Because there are 25.4 millimeters in an inch, so we convert mm to inches and multiply by PPI.

The line having logmar = 0 is set as the normal vision line and rest lines have been calculated by a logmar increment of 0.1 for everyline. And the logmar is converted to diopters assuming a linear division dependence to get approximately accurate results. The multiplied constant would be recaliberated on further testing.

This gives the actual pixel height for each letter on that line.

🧾 Step 5: Rendering the Snellen Chart
The script loops through the lines and applies the computed fontSize in pixels to each one:

javascript

div.style.fontSize = pixelSizes[index] + 'px';
div.textContent = line;
Each line is styled and appended to the chart container with proper alignment and optional highlighting.

🧪 Step 6: Submitting a Line Number to Predict Diopter
After the chart is rendered, a second form appears where the user can select the last line they were able to read:

html

<form id="lineForm" method="POST" action="{% url 'predict_diopters' %}">
This value is sent to the Django backend to calculate and return the approximate diopter value.

📄 Step 7: Generating a PDF with Correct Font Sizes
On clicking Download PDF, the app:

Reconstructs the chart in a temporary DOM element.

Applies the same pixel sizes as on screen.

Highlights the selected line (if any).

Uses html2pdf.js to save it as a downloadable PDF.

javascript

await html2pdf().set(opt).from(pdfContent).save();
PDF includes all lines and preserves font scaling for printing or sharing.

🔲 Step 8: Fullscreen Mode
Clicking the "Go Fullscreen" button triggers fullscreen mode via the browser's Fullscreen API:

javascript

document.documentElement.requestFullscreen();
This allows better visibility when taking the Snellen test.

🌗 Step 9: Theme Toggle and Dark Mode
The app has a theme toggle switch that adds or removes the dark-mode class:

javascript

themeToggle.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
});
It also respects the system's preferred theme:

javascript

if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.body.classList.add('dark-mode');
}
🔐 CSRF Token Handling (for Django)
The JavaScript includes a utility function to fetch the CSRF token from cookies for Django POST requests:

javascript

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const c = cookie.trim();
        if (c.startsWith(name + '=')) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return '';
}
📦 Technologies Used
HTML5, CSS3, Vanilla JavaScript

Browser Fullscreen API

html2pdf.js library

Django (backend for diopter prediction)

Responsive design with dynamic DOM rendering

🧪 Example Flow
User enters diagonal size (e.g., 15.6 inches).

Script detects screen resolution (e.g., 1920×1080).

Calculates PPI.

Computes pixel sizes for each of the 15 Snellen lines.

Displays the chart with correctly sized letters.

User selects the last line they can read.

App sends line number to backend to estimate diopter.

User can export the chart as PDF or view it in fullscreen.

📌 Notes
This app is intended for educational or demonstration purposes.

For real-world eye exams, consult with a licensed optometrist.

Character sizing is accurate only if diagonal size is entered correctly.
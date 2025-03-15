document.addEventListener("DOMContentLoaded", () => {
    const keys = document.querySelectorAll(".white-key, .black-key");

    const sound = {
        // Map of keycodes to sound URLs
        65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
        87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
        83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
        69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
        68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
        70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
        84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
        71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
        89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
        72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
        85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
        74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
        75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
        79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
        76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
        80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
        186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
    };

    keys.forEach(key => {
        key.addEventListener("mouseover", () => {
            const keyLabel = key.dataset.key;
            const labelElement = key.querySelector(".key-label");
            if (labelElement && keyLabel) {
                labelElement.textContent = keyLabel; // Display key label on hover
            }
        });

        key.addEventListener("mouseout", () => {
            const labelElement = key.querySelector(".key-label");
            if (labelElement) {
                labelElement.textContent = ""; // Remove label when mouse leaves
            }
        });

        key.addEventListener("click", (event) => {
            if (event.button === 0) { // Check for left-click
                console.log('Key clicked:', key);
                key.classList.add("pressed"); // Add pressed class for visual effect
                setTimeout(() => key.classList.remove("pressed"), 100); // Remove after 100ms

                const keyLabel = key.dataset.key;
                const soundUrl = sound[keyLabel.charCodeAt(0)];
                if (soundUrl) {
                    const audio = new Audio(soundUrl);
                    audio.play(); // Play sound
                }
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    let secretInput = "";
    const secretCode = "WESEEYOU";
    let secretActivated = false;

    function activateGreatOldOne() {
        if (secretActivated) return;
        secretActivated = true;

        const audio = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");
        audio.play();

        const pianoContainer = document.querySelector(".piano") || document.body;
        pianoContainer.style.pointerEvents = "none";

        pianoContainer.style.transition = "opacity 3s";
        pianoContainer.style.opacity = "0";

        setTimeout(() => {
            pianoContainer.innerHTML = ""; // Clear piano container after transition

            pianoContainer.style.opacity = "1";

            const img = document.createElement("img");
            img.src = "/static/piano/images/texture.jpeg";  // Update path
            img.alt = "The Great Old One";

            img.style.maxWidth = "600px";
            img.style.width = "100%";
            img.style.height = "auto";
            img.style.display = "block";
            img.style.margin = "0 auto";

            img.style.opacity = "0";
            img.style.transition = "opacity 3s";

            pianoContainer.appendChild(img);
            setTimeout(() => {
                img.style.opacity = "1"; // Fade in image 
            }, 50);
        }, 3000);
    }

    document.addEventListener("keydown", (e) => {
        if (secretActivated) return;
        secretInput += e.key.toUpperCase();

        if (secretInput.length > secretCode.length) {
            secretInput = secretInput.slice(-secretCode.length);
        }

        if (secretInput === secretCode) {
            activateGreatOldOne(); // Activate secret event 
        }
    });

    const keys = document.querySelectorAll(".white-key, .black-key");
    keys.forEach((key) => {
        key.addEventListener("click", () => {
            if (secretActivated) return;
            const keyLetter = key.dataset.key;
            if (keyLetter) {
                secretInput += keyLetter.toUpperCase();
                if (secretInput.length > secretCode.length) {
                    secretInput = secretInput.slice(-secretCode.length);
                }
                if (secretInput === secretCode) {
                    activateGreatOldOne(); // Trigger secret event if code match
                }
            }
        });
    });
});

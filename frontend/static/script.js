document.addEventListener("DOMContentLoaded", () => {
    const btnUpload = document.getElementById("btn-upload");
    const btnWebcam = document.getElementById("btn-webcam");
    const uploadSection = document.getElementById("upload-section");
    const webcamSection = document.getElementById("webcam-section");
    
    btnUpload.addEventListener("click", () => {
        btnUpload.classList.add("active");
        btnWebcam.classList.remove("active");
        uploadSection.classList.add("active");
        uploadSection.classList.remove("hidden");
        webcamSection.classList.remove("active");
        webcamSection.classList.add("hidden");
        stopWebcam();
    });

    btnWebcam.addEventListener("click", () => {
        btnWebcam.classList.add("active");
        btnUpload.classList.remove("active");
        webcamSection.classList.add("active");
        webcamSection.classList.remove("hidden");
        uploadSection.classList.remove("active");
        uploadSection.classList.add("hidden");
    });

    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("file-input");
    const previewImage = document.getElementById("preview-image");
    const loading = document.getElementById("loading");
    
    const predLabel = document.getElementById("pred-label");
    const confidenceBar = document.getElementById("confidence-bar");
    const predConf = document.getElementById("pred-conf");
    const predFps = document.getElementById("pred-fps");

    dropArea.addEventListener("click", () => fileInput.click());

    dropArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropArea.classList.add("dragover");
    });

    dropArea.addEventListener("dragleave", () => {
        dropArea.classList.remove("dragover");
    });

    dropArea.addEventListener("drop", (e) => {
        e.preventDefault();
        dropArea.classList.remove("dragover");
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFile(fileInput.files[0]);
        }
    });

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length) {
            handleFile(fileInput.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.startsWith("image/")) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewImage.hidden = false;
            uploadImage(file);
        };
        reader.readAsDataURL(file);
    }

    async function uploadImage(file) {
        loading.hidden = false;
        
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/predict-image", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            updateResults(data);
        } catch (error) {
            console.error("Error predicting:", error);
            predLabel.innerText = "Error";
        } finally {
            loading.hidden = true;
        }
    }

    function updateResults(data) {
        predLabel.innerText = data.label;
        const confPercent = (data.confidence * 100).toFixed(1);
        confidenceBar.style.width = `${confPercent}%`;
        predConf.innerText = `${confPercent}%`;
        predFps.innerText = data.fps ? data.fps.toFixed(1) : "-";
        
        predLabel.style.transform = "scale(1.1)";
        setTimeout(() => {
            predLabel.style.transform = "scale(1)";
            predLabel.style.transition = "transform 0.3s ease";
        }, 150);
    }

    const btnStartWebcam = document.getElementById("start-webcam");
    const btnStopWebcam = document.getElementById("stop-webcam");
    const videoFeed = document.getElementById("video-feed");

    btnStartWebcam.addEventListener("click", () => {
        videoFeed.src = "/video_feed";
        
        predLabel.innerText = "Live On Video Feed";
        confidenceBar.style.width = "100%";
        predConf.innerText = "See Video";
        predFps.innerText = "-";
    });

    btnStopWebcam.addEventListener("click", () => {
        stopWebcam();
    });

    function stopWebcam() {
        videoFeed.src = "";
        predLabel.innerText = "-";
        confidenceBar.style.width = "0%";
        predConf.innerText = "0%";
        predFps.innerText = "-";
    }
});

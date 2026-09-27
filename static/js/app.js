const input =
    document.getElementById("imageInput");

const uploadZone =
    document.getElementById("uploadZone");

const fileName =
    document.getElementById("fileName");

const fileInfo =
    document.getElementById("fileInfo");

const previewContainer =
    document.getElementById("previewContainer");

const previewImage =
    document.getElementById("previewImage");

const scanButton =
    document.getElementById("scanButton");

const uploadForm =
    document.getElementById("uploadForm");


/* ======================================================
   FILE SELECTION
====================================================== */

if (input) {

    input.addEventListener(
        "change",
        function () {

            const file =
                this.files[0];

            if (!file) {
                return;
            }

            showFile(file);

        }
    );

}


/* ======================================================
   DRAG & DROP
====================================================== */

if (uploadZone) {

    uploadZone.addEventListener(
        "dragover",
        function (event) {

            event.preventDefault();

            uploadZone.style.borderColor =
                "#f0a52b";

            uploadZone.style.background =
                "#11171a";

        }
    );


    uploadZone.addEventListener(
        "dragleave",
        function () {

            uploadZone.style.borderColor =
                "";

            uploadZone.style.background =
                "";

        }
    );


    uploadZone.addEventListener(
        "drop",
        function (event) {

            event.preventDefault();

            uploadZone.style.borderColor =
                "";

            const file =
                event.dataTransfer.files[0];

            if (!file) {
                return;
            }


            /*
             * Put dropped file into the
             * actual file input.
             */

            const dataTransfer =
                new DataTransfer();

            dataTransfer.items.add(file);

            input.files =
                dataTransfer.files;


            showFile(file);

        }
    );

}


/* ======================================================
   SHOW SELECTED FILE
====================================================== */

function showFile(file) {

    fileName.textContent =
        file.name.toUpperCase();

    const size =
        file.size / 1024 / 1024;

    fileInfo.textContent =
        size.toFixed(2) +
        " MB  /  INSPECTION FRAME READY";


    previewImage.src =
        URL.createObjectURL(file);


    previewContainer.style.display =
        "block";


    scanButton.style.display =
        "flex";


    scanButton.querySelector("span")
        .textContent =
        "RUN MINESPIDER AI";

}


/* ======================================================
   FORM SUBMIT
====================================================== */

if (uploadForm) {

    uploadForm.addEventListener(
        "submit",
        function () {

            scanButton.disabled =
                true;


            scanButton.querySelector("span")
                .textContent =
                "ANALYZING FRAME...";


            scanButton.querySelector("b")
                .textContent =
                "◌";

        }
    );

}
!function () {

    String.prototype.format = function() {
        let that = this;
        for (let k in arguments) {
            that = that.replace("{" + k + "}", arguments[k])
        }
        return that;
    };

    let App = {};

    let services = {
        fileUpload: '/upload'
    };

    App.attachEvents = function() {
        window.addEventListener("dragover",function(e){
            e = e || event;
            e.preventDefault();
        },false);
        window.addEventListener("drop",function(e){
            e = e || event;
            e.preventDefault();
        },false);
        let dropArea = document.getElementById('drop-area');
        dropArea.addEventListener('drop', App.handleDrop, false);
        //prevent default behavior
        dropArea.addEventListener('drag', App.preventDefaults, false);
        dropArea.addEventListener('dragstart', App.preventDefaults, false);
        dropArea.addEventListener('dragend', App.preventDefaults, false);
        dropArea.addEventListener('dragover', App.preventDefaults, false);
        dropArea.addEventListener('dragenter', App.preventDefaults, false);
        dropArea.addEventListener('dragleave', App.preventDefaults, false);
        dropArea.addEventListener('drop', App.preventDefaults, false);
        //highlight events
        dropArea.addEventListener('dragenter', App.highlight, false);
        dropArea.addEventListener('dragover', App.highlight, false);
        //unhighlight
        dropArea.addEventListener('dragleave', App.unhighlight, false);
        dropArea.addEventListener('drop', App.unhighlight, false);
    };

    App.dragEnter = function(e) {
        console.log("Drag Enter")
    };

    App.highlight = function(e) {
        let dropArea = e.target;
        dropArea.classList.add('highlight')
    };

    App.unhighlight = function(e) {
        let dropArea = e.target;
        dropArea.classList.remove('highlight')
    };

    App.prevantDefaults = function(e) {
        e.preventDefault();
        e.stopPropagation();
    };

    App.handleDrop = function(e) {
        let dt = e.dataTransfer;
        let files = dt.files;
        ([...files]).forEach(App.uploadFile)
    };

    App.uploadFile = function(file) {
        let url = services.fileUpload;
        let xhr = new XMLHttpRequest();
        let formData = new FormData();
        xhr.open('POST', url, true);
        xhr.addEventListener('readystatechange', function(e) {
            if (xhr.readyState == 4 && xhr.status == 200) {
                console.log("File uploaded successfully");
            }
            else if (xhr.readyState == 4 && xhr.status != 200) {
                console.log("File upload failed");
            }
        });
        formData.append('file', file);
        xhr.send(formData)
    };

    App.run = function() {
        App.attachEvents();
    };

    App.fetchTable = function() {
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/pdf', true);
        xhr.addEventListener('readystatechange', function(e) {
            if (xhr.readyState == 4 && xhr.status == 200) {
                App.buildTable(xhr.responseText);
            }
            else if (xhr.readyState == 4 && xhr.status != 200) {
                console.log("File upload failed");
            }
        });
        xhr.send();
    };

    App.modifyTable = function(nodes, key, res) {
        let it, len;
        nodes[1].innerHTML += key;
            nodes[3].innerHTML += res['page_count'];
            if (res['page_diff_flag']) {
                nodes[5].childNodes[0].classList.add("highlight-green");
            }
            else {
                nodes[5].childNodes[0].classList.add("highlight-red");
            }
            for (it = 0, len = res['annotations_list'].length; it < len; it++) {
                nodes[7].innerHTML += res['annotations_list'][it];
            }
            if (res['annotations_flag']) {
                nodes[9].childNodes[0].classList.add("highlight-green");
            }
            else {
                nodes[9].childNodes[0].classList.add("highlight-red");
            }
            if (res['signature_present']) {
                nodes[11].childNodes[0].classList.add("highlight-green");
            }
            else {
                nodes[11].childNodes[0].classList.add("highlight-red");
            }
            if (res['markup_present']) {
                nodes[13].childNodes[0].classList.add("highlight-green");
            }
            else {
                nodes[13].childNodes[0].classList.add("highlight-red");
            }
            if (res['send_through']) {
                nodes[15].childNodes[0].classList.add("highlight-green");
            }
            else {
                nodes[15].childNodes[0].classList.add("highlight-red");
            }
    };

    App.buildTable = function(response) {
        let frag;
        response = JSON.parse(response);
        let bottomContainer = document.getElementById("container-bottom");
        let header = '<div class="header">' +
            '            <div style="width: 18%">Files</div>' +
            '            <div style="width: 8%">Pages</div>' +
            '            <div style="width: 8%">Match</div>' +
            '            <div style="width: 30%">Annotation</div>' +
            '            <div style="width: 8%">Changed</div>' +
            '            <div style="width: 8%">Signed</div>' +
            '            <div style="width: 8%">Markup</div>' +
            '            <div>Send Through</div>    ' +
            '        </div>';
        frag = document.createRange().createContextualFragment(header);
        bottomContainer.appendChild(frag);
        let row = '<div class="combined-row">' +
            '            <div class="row" id="top-row">' +
            '                <div style="width: 18%"></div>' +
            '                <div style="width: 8%"></div>' +
            '                <div style="width: 8%"><div class="signal-top"></div></div>' +
            '                <div style="width: 30%"></div>' +
            '                <div style="width: 8%"><div class="signal-top"></div></div>' +
            '                <div style="width: 8%"><div class="signal-top"></div></div>' +
            '                <div style="width: 8%"><div class="signal-top"></div></div>' +
            '                <div style="width: 8%"><div class="signal-top"></div></div>' +
            '            </div>' +
            '            <div class="row" id="bottom-row">' +
            '                <div style="width: 18%"></div>' +
            '                <div style="width: 8%"></div>' +
            '                <div style="width: 8%"><div class="signal-bottom"></div></div>' +
            '                <div style="width: 30%"></div>' +
            '                <div style="width: 8%"><div class="signal-bottom"></div></div>' +
            '                <div style="width: 8%"><div class="signal-bottom"></div></div>' +
            '                <div style="width: 8%"><div class="signal-bottom"></div></div>' +
            '                <div style="width: 8%"><div class="signal-bottom"></div></div>' +
            '            </div>' +
            '        </div>';
        let nodes, key, res, it, len, a, b;
        let entries = Object.entries(Object.entries(response));
        for(it = 0; it <entries.length; it+=2) {
            a = entries[it][1];
            b = entries[it+1][1];
            frag = document.createRange().createContextualFragment(row);
            nodes = frag.getElementById("top-row").childNodes;
            App.modifyTable(nodes, a[0], a[1]);
            nodes = frag.getElementById("bottom-row").childNodes;
            App.modifyTable(nodes, b[0], b[1]);
            bottomContainer.appendChild(frag);
        }
    };

    App.run();
    App.fetchTable();
}();
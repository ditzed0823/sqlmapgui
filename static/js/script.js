
function showLoadingScreen() {
    document.getElementById('loadingScreen').style.display = 'flex';
}

function hideLoadingScreen() {
    document.getElementById('loadingScreen').style.display = 'none';
}

document.getElementById('generateCommand').addEventListener('click', function() {
    const formData = new FormData(document.getElementById('targetForm'));
    const dbData = new FormData(document.getElementById('injectionSettingsForm'));
    const enumerationData = new FormData(document.getElementById('enumerationForm'));
    showLoadingScreen();

    const allData = new FormData();
    formData.forEach((value, key) => allData.append(key, value));
    dbData.forEach((value, key) => allData.append(key, value));
    tableData.forEach((value, key) => allData.append(key, value));
    enumerationData.forEach((value, key) => allData.append(key, value));

    fetch('/generate-command', {
        method: 'POST',
        body: allData
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingScreen();

        if (data.error) {
            alert("Error: " + data.error);
        } else {
            document.getElementById('generatedCommand').textContent = data.command;
            document.getElementById('commandSection').classList.remove('hidden');
            runCommand();
        }
    })
    .catch(error => {
        hideLoadingScreen();
        alert("Error: " + error);
    });
});

function runCommand() {
    showLoadingScreen();

    fetch('/run-command', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingScreen();

        if (data.error) {
            document.getElementById('output').textContent = "Error: " + data.error;
        } else {
            document.getElementById('output').textContent = data.output;
        }
    })
    .catch(error => {
        hideLoadingScreen();
        document.getElementById('output').textContent = "Error: " + error;
    });
}

document.getElementById('runCommand').addEventListener('click', function() {
    showLoadingScreen();

    fetch('/run-command', {
    method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
    hideLoadingScreen();

    if (data.error) {
        document.getElementById('output').textContent = "Error: " + data.error;
    } else {
        document.getElementById('output').textContent = data.output;
    }
    })
    .catch(error => {
    hideLoadingScreen();
    document.getElementById('output').textContent = "Error: " + error;
    });
});

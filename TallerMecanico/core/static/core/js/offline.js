function updateNetworkStatus() {
    const box = document.getElementById("network-status");

    if (!navigator.onLine) {
        box.classList.remove("d-none");
    } else {
        box.classList.add("d-none");
    }
}

window.addEventListener("load", updateNetworkStatus);
window.addEventListener("online", updateNetworkStatus);
window.addEventListener("offline", updateNetworkStatus);

$('#cmdRoll').click(function (e) {
    e.preventDefault();
    console.log("Rock 'n' roll!");

    $.post("/play", {
        nonce: nonce,
        seed: clientseed
    }).done(function (res) {
        location.reload();
    }).fail(function (err) {
        console.log(err);
        alert("Roll failed: " + err.status + " - " + err.responseText);
        location.reload();
    });
});
// vulnerable_xss.js
const processUserData = () => {
    //  PELIGRO: Obtener datos directamente de la URL sin sanitizar
    const params = window.location.search.substring(1).split("&");
    const userObj = {};

    for (const i = 0; i < params.length; i++) {
        const pair = params[i].split("=");
        
        // Complejidad artificial para disparar la métrica de Lizard
        if (pair.length > 1) {
            while(pair[1].indexOf("%20") > -1) {
                pair[1] = pair[1].replace("%20", " ");
                if (pair[1].length > 1000) break; 
            }
            //  PELIGRO: Uso de eval() para parsear datos (Inyección de código)
            try {
                if (pair[0] == "config") {
                    eval("const config = " + pair[1]);
                }
            } catch(e) { console.log(e); }

            userObj[pair[0]] = pair[1];
        }
    }

    //  PELIGRO: DOM Based XSS (Cross Site Scripting)
    // Inserta HTML directo del usuario en la página
    const displayDiv = document.getElementById("user-display");
    if (userObj.name) {
        displayDiv.innerHTML = "<h1>Welcome " + userObj.name + "</h1>";
    }

    //  PELIGRO: document.write es obsoconsto y peligroso
    document.write("DEBUG: " + JSON.stringify(userObj));
}
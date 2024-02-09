function inventario(){
    $.ajax({
        url:"/inventario",
        data: {
            form:$("form").serialize()
        },
        type:"get",
        contentType:"application/json",
        dataType:"json",
        success:function(data){
            document.getElementById("productos").innerHTML = data['text'];
        }
     });
}
var serached;
function despacho(){
    serached = $("form").serialize().split("&")[3].split("=")[1];
    console.log(serached)
    $.ajax({
        url:"/despacho",
        data: {
            form:serached
        },
        type:"get",
        contentType:"application/json",
        dataType:"json",
        success:function(data){
            document.getElementById("busquedas").innerHTML = data['text'];
        }
     });
}

function despachar(solicitud,solicitudD){
    $.ajax({
        url:"/despacho",
        data: {
            form:serached,
            nombre: document.getElementById("nombre_despachante").value,
            ci: document.getElementById("ci_despachante").value,
            id:solicitud,
            sol_de:solicitudD
        },
        type:"get",
        contentType:"application/json",
        dataType:"json",
        success:function(data){
            document.getElementById("busquedas").innerHTML = data['text'];
        }
     });
}

function despachar_todo(){
    let ids = document.querySelectorAll('.target-despacho a');
    let id_sd = "";
    for (let i = 0; i < ids.length; i++) {
        id_sd += ids[i].id+ ",";
    }
    id_s = document.getElementById('form-despacho-search').value
    $.ajax({
        url:"/despacho",
        data: {
            form:serached,
            nombre: document.getElementById("nombre_despachante").value,
            ci: document.getElementById("ci_despachante").value,
            id:id_s,
            sol_de:id_sd,
        },
        type:"get",
        contentType:"application/json",
        dataType:"json",
        success:function(data){
            document.getElementById("busquedas").innerHTML = data['text'];
        }
     });
}

function solicitar_productos(fig, nombre_producto) {
    $.ajax({
        url:"/empleados/solicitar",
        data: {
            id_tp:fig
        },
        type:"get",
        contentType:"application/json",
        dataType:"json",
        success:function(data){
            document.getElementById("productos").innerHTML = data['text'];
        }
    });
}

var carrito = [];

function agregar_carrito(...productos){
    document.getElementById('carrito-table').style.display = "block";
    let cantidad = document.getElementById('catidad_id'+productos[0]).value;
    carrito.push({
        id:productos[0],
        nombre:productos[1],
        cantidad,
        precio:productos[2],
        total:cantidad*productos[2]
    });
    document.getElementById('catidad_id'+productos[0]).value = "";

    
    let total = 0;
    document.getElementById('carrito-table-tbody').innerHTML = "";
    for(let i = 0; i < carrito.length; i++){
        document.getElementById('carrito-table-tbody').innerHTML += "<tr><td>"+carrito[i].nombre+"</td><td>"+carrito[i].cantidad+"</td><td>"+carrito[i].precio+"</td><td>"+carrito[i].total+"</td></tr>";
        total += carrito[i].total;
    }
    
    document.getElementById('carrito-table-tfoot').innerHTML = "<tr><td colspan='4'>Total: "+total+"</td></tr>";
    
}

function insertar_solicitud() {
    let cantidades = "";
    let id_productos = "";
    for(let i = 0; i < carrito.length; i++){
        cantidades += carrito[i].cantidad+"-";
        id_productos += carrito[i].id+"-";
    }
    titulo = document.getElementById('form-title').value

    $.ajax({
        url:"/empleados/solicitar",
        data: {
            id_tp:false,
            titulo,
            cantidades,
            observaciones:"rapidon",
            id_productos
        },
        type:"get",
        contentType:"application/json",
        dataType:"json",
        success:function(data){
            setTimeout(function(){
                window.location.href = "http://127.0.0.1:5000/index";
            }, 5 * 1000);
        }
    });
}
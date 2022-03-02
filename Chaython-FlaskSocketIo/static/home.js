/*******************************************************VARIABLES GLOBALES*******************************************************/
const rooms_cont = document.getElementById('rooms_cont');
const chats_cont = document.getElementById('chats_cont');
const array_actions = ['create', 'join'];
const buttons = document.getElementsByClassName('btn-block');


/*******************************************************FUNCIONES*******************************************************/
function prepararListeners(){
    logout.addEventListener('click', function(){window.location.href = '/logout'});
    searchPerson.addEventListener('click', function(){
        const personalNumber = pchatname.value;
        if (personalNumber == '') {
            alert('El número de la persona no puede estar vacio');
            return;
        }
        findPerson(personalNumber)
    });
    closepersonalchat.addEventListener('click', displayAddPersonalChat);
    addpersonalchat.addEventListener('click', displayAddPersonalChat);
}

function displayAddPersonalChat(){
    addchatcont.classList.toggle('hidden');
    pchatname.focus();
    pchatname.value = '';
}

function innerHTMLTo(conteiner, elements){
    for (let i = 0; i < elements.length; i++) {
        conteiner.innerHTML+=elements[i];
    }
    prepararListeners();
}

// TODO: Cambiar metodos para llamar a un chat privado (hacer el metodo en python)
function buildChatStructure(chatsjs){
    let chatstr;
    // console.log(chatsjs[0]['_id']['$oid']);
    let rooms = []
    for (let i = 0; i < chatsjs.length; i++) {
        chatstr = "<div class='chat'>"
        chatstr += "<div class='chat-info'>"
        chatstr += "<p class='chat-name font_strong'>"+chatsjs[i]['otherUserName']+"</p>"
        chatstr += "<p class='chat-code'>CHAT PRIVADO</p>"
        chatstr += "</div>"
        chatstr += "<form action='/Chaython/private' method='POST'>"
        chatstr += "<button class='chat-join default-press-hover'>ENTRAR</button>"
        chatstr += "<input type='hidden' name='chat' value='"+chatsjs[i]['_id']['$oid']+"'>"
        chatstr += "<input type='hidden' value='"+chatsjs[i]['otherUserName']+"' name='connect_to'>"
        chatstr += "</form>"
        chatstr += "</div>"
        rooms.push(chatstr)
    }
    return rooms;
}

function buildRoomStructure(roomsjs){
    let chatstr;
    let rooms = []
    for (let i = 0; i < roomsjs.length; i++) {
        chatstr = "<div class='chat'>"
        chatstr += "<div class='chat-info'>"
        chatstr += "<p class='chat-name font_strong'>"+roomsjs[i]['name']+"</p>"
        chatstr += "<p class='chat-code'>"+roomsjs[i]['code']+"</p>"
        chatstr += "</div>"
        chatstr += "<form action='/Chaython' method='POST'>"
        chatstr += "<button class='chat-join default-press-hover'>ENTRAR</button>"
        chatstr += "<input type='hidden' name='room' value='"+roomsjs[i]['code']+"'>"
        chatstr += "<input type='hidden' value='join' name='room_action'>"
        chatstr += "</form>"
        chatstr += "</div>"
        rooms.push(chatstr)
    }
    return rooms;
}

function findPerson(personalNumber){
    fetch("/chat/"+personalNumber)
    .then((resp) => resp.json())
    .then(function(data) {
        return checkPerson(data);
    })
    .catch(function(error) {
        console.log(error);
    });
    
}

function checkPerson(p){
    const person = p;
    if (person == null) {
        alert('La persona con el numero indicado no existe');
        return;
    }
    console.log(person);
    let notificacion = '<div class="addchat-notification">';
    notificacion += '    <p>¿Seguro que quiere añadir a <b>%%name%%</b> a su lista de chats privados?</p>';
    notificacion += '   <button id="btnaddchat" class="btn btn-lg btn-primary btn-block">Agregar</button>';
    notificacion += '   <button id="btncanceladdchat" class="btn btn-lg btn-secondary btn-block">Cancelar</button>';
    notificacion += '</div>';
    notifier.innerHTML = notificacion.replace('%%name%%', person.name);
    btncanceladdchat.addEventListener('click', function(){
        this.parentElement.remove();
    });
    btnaddchat.addEventListener('click', function(){
        addPrivateChat(person);
        this.parentElement.remove();
        addchatcont.classList.add('hidden');
    });
}

function addPrivateChat(user){
    fetch("/chat/add/"+user.code)
    .then((resp) => resp.json())
    .then(function(data) {
        if (data == -2){
            alert('No puede iniciar un chat privado consigo mismo.');
            return;
        }
        return location.reload();
    })
    .catch(function(error) {
        console.log(error);
    });
}

/*******************************************************CODE*******************************************************/


fetch("/rooms")
.then((resp) => resp.json())
.then(function(data) {
    return innerHTMLTo(rooms_cont, buildRoomStructure(data))
})
.catch(function(error) {
    console.log(error);
});

fetch("/chats")
.then((resp) => resp.json())
.then(function(data) {
    return innerHTMLTo(chats_cont, buildChatStructure(data))
})
.catch(function(error) {
    console.log(error);
});

for (let index = 0; index < 2; index++) {
    const uname = document.getElementById('user_name').innerHTML;
    const name_letter = uname.charAt(0).toUpperCase();
    document.getElementById('name_letter').textContent = name_letter;

    buttons[index].addEventListener('click', function () {
        const roomName = document.getElementById('RoomName').value;
        if (roomName == '') {
            alert('El nombre de la sala no puede estar vacia');
            preventDefault();
        }
        else {
            document.getElementById('room_action').value = array_actions[index];
        }
    });
}

document.addEventListener('DOMContentLoaded', function(){
    prepararListeners();
});
const url = 'http://127.0.0.1:5000/';
const rooms_cont = document.getElementById('rooms_cont');
const chats_cont = document.getElementById('chats_cont');

fetch("/rooms")
.then((resp) => resp.json())
.then(function(data) {
    return innerHTMLTo(rooms_cont, buildChatStructure(data))
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

function innerHTMLTo(conteiner, elements){
    for (let i = 0; i < elements.length; i++) {
        conteiner.innerHTML+=elements[i];
    }
}

function buildChatStructure(roomsjs){
    let chatstr;
    let rooms = []
    for (let i = 0; i < roomsjs.length; i++) {
        chatstr = "<div class='chat'>"
        chatstr += "<div class='chat-info'>"
        chatstr += "<p class='chat-name font_strong'>"+roomsjs[i]['name']+"</p>"
        chatstr += "<p class='chat-code'>"+roomsjs[i]['_id']+"</p>"
        chatstr += "</div>"
        chatstr += "<form action='/Chaython' method='POST'>"
        chatstr += "<button class='chat-join'>ENTRAR</button>"
        chatstr += "<input type='hidden' name='room' value='"+roomsjs[i]['_id']+"'>"
        chatstr += "<input type='hidden' value='join' name='room_action'>"
        chatstr += "</form>"
        chatstr += "</div>"
        rooms.push(chatstr)
    }
    return rooms;
}

const array_actions = ['create', 'join'];
const buttons = document.getElementsByClassName('btn-block');
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
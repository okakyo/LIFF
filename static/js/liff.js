const Device_UUID='';
const Characteristic_UUID='';


window.onload = ()=>{
    initializeApp();
};

function handlerApp() {
    return;
};
function initializeApp() {
    liff.init(()=>initializeLiff(),error=>uiStatusError(makeErrorMsg(error),false));
};
function initializeLiff() {
    liff.initPlugins(['bluetooth']).then(()=>{
       liffCheckaAvailablityAndDo(()=>liffRequestDevice());
    }).catch(()=>{
        uiStatusError(makeErrorMsg(error),false);
    })
};
function handlerApp() {
    return;
};
function handlerApp() {
    return;
};
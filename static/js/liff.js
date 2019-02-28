const Device_UUID='';
const Characteristic_UUID='';


window.onload = ()=>{
    initializeApp();
};

function handlerApp() {
    return;
};

function makeErrorMsg(e){
    return "Error!\n"+e.code+"\n"+e.message;
}

function uiStatusError(e,showAnimation){
    uiToggleLoadingAnimation(showAnimation);
    
    const elStatus=document.getElementById('status');
    const elControls=document.getElementById('controls');
    
    elStatus.classList.remove('success');
    elStatus.classList.remove('inactive');
    elStatus.classList.add('error');
    elStatus.innerText=e;

    elControls.classList.add('hidden');
}

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
function liffCheckaAvailablityAndDo(callbackIfAvailable) {
    liff.bluetooth.getAvailablity().then((check)=> {
        if (check){
            callbackIfAvailable();
        }
        else{
            setTimeout(()=>liffCheckaAvailablityAndDo(callbackIfAvailable),10000);
        }
    }).catch(e => {
        uiStatusError(makeErrorMsg(e),false);
    })
};
function liffRequestDevice(){
    liff.bluetooth.requestDevice().then(device =>{
          liffConnectToDevice(device);
    }).catch(e=>{
        uiStatusError(makeErrorMsg(e),false);
    })
}

function liffConnectToDevice(device){
    device.gatt.connect().then(()=>{
        document.getElementById('device_name').innerText=device.name;
        document.getElementById('device_id').innerText=device.id;

        uiToggleDeviceConnected(true);

        device.gatt.getPrimaryService(USER_SERVICE_UUID).then(service =>{
            liffGetUserService(service);
        }).catch(e =>{uiStatusError(makeErrorMsg(e),false);
        });
    

        device.gatt.getPrimaryService(PSDI_SERVICE_UUID).then(service =>{
            liffGetPSDIService(service);
        }).catch(e =>{uiStatusError(makeErrorMsg(e),false);
        });
    
    const disConnectCallback= ()=>{
        uiToggleDeviceConnected(false);
        device.removeEventListener('GATTServiceDisconnecnted',disConnectCallback);

        ledState=false;

        uiToggleButton(false);
        uiToggleStatebutton(false);

        initializeLiff();
    };
    device.addEventListener('GATTServerDisconnected',disConnectCallback);
}).catch(e=>{
    uiStatusError(makeErrorMsg(e),false);
});
}

function liffGetUserService(service){
    service.gatt.getCharacteristic(USER_SERVICE_UUID).then().catch(e =>{uiStatusError(makeErrorMsg(e),false)})
    service.gatt.getCharacteristic(USER_SERVICE_UUID).then().catch(e =>{uiStatusError(makeErrorMsg(e),false)})
}
function liffGetPSDIService(service){
    service.gatt.getCharacteristic(Characteristic_UUID).then().catch(e =>{uiStatusError(makeErrorMsg(e),false)})
}
function closeResistration(){
    for(let i=0;i<2;i++){
        document.getElementsByClassName('modal')[i].style.display = 'none';
    }
    try{
        document.getElementsByClassName('studentDetails')[0].style.display = 'none';
    }
    catch{
        pass;
    }
}

const renderData = (tagname, value) =>{
    let tagis = document.getElementById(tagname);
    if(tagis){
        if(tagname == 'sphoto'){
            tagis.src = value;
        }
        else
            tagis.value = value;
    }
}

const populateStudentData = (data) =>{
    renderData('rollNumber',data['rollNumber'])
    renderData('firstName',data['first Name'])
    renderData('lastName',data['last Name']);
    renderData('fname',data['father Name']);
    renderData('mname',data['mother Name']);
    renderData('mname',data['mother Name'])
    renderData('dob', data['dob']);
    renderData('contactNumber',data['mobile']);
    renderData('parentContact',data['pmobile']);
    renderData('sphoto',data['photo']);
    renderData('address',data['Address']);

    document.getElementsByClassName('studentDetails')[0].style.display = 'block';
}

const fetchStudent = (sron) =>{
    let xhs = new XMLHttpRequest();
    xhs.open('POST','fetchstudent', true)
    xhs.setRequestHeader('X-CSRFToken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
    xhs.send(JSON.stringify({rollno : sron}));
    xhs.onreadystatechange = function () {

        var data = JSON.parse(this.responseText);
        console.log(data)
        populateStudentData(data)
    }
}

// event listner to search student, when admit hit enter, details of student will be fetched
window.onload=function(){
    var input = document.getElementById("searchStudent");
    input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        fetchStudent(input.value);
        }
    })
}
document.addEventListener('DOMContentLoaded', function() {
brands_shown = []
let box = document.createElement("div");
box.style.display = "none"
document.querySelector('#para').append(box);
box.id = "filterBox"
get_posts()
document.querySelector('#filter').addEventListener("click", show_box)


function change_posts(brand){
    
    if(brands_shown.includes(brand)){
        //moving element to last index
        let index = brands_shown.indexOf(brand)
        let temp = brands_shown[brands_shown.length - 1]
        brands_shown[brands_shown.length - 1] = brands_shown[index]
        brands_shown[index] = temp

        brands_shown.pop()
    }
    else{
        brands_shown.push(brand)
    } 
    const params = {
        brands: brands_shown
    };
    const options = {
        method: 'POST',
        body: JSON.stringify( params )  }

    fetch('/brands', options)
    .then(response => response.json())
    .then(result => {
    
        document.querySelector('#articles').innerHTML = ""
        load_posts(result)
    })

}

function show_box(){
    
    if (box.style.display == "none"){
        
        box.style.display = "block"
        filter()
    }
    else{
        box.style.display = "none"
    }
    
}

function filter(){
    box.innerHTML = ""
    fetch("/filter", {
        method: "POST"
    })
    .then(response => response.json())
    .then(result => {
        for(let i =0; i<result["Length"]; i++){
            input_check = document.createElement('input')
            input_check.type = "checkbox"
            input_check.id = result[i]
            input_check.class = "filterButton"
            input_check.value = 1
            box.append(input_check)
            input_check.addEventListener('click', () => change_posts(result[i]));
            label = document.createElement('label')
            label.innerHTML = result[i]
            label.for = result[i]
            box.append(label)

            let linebreak = document.createElement('br')
            box.append(linebreak)
        }
      
      
    })

}
function get_posts(){
    fetch("/allposts", {
        method: "POST"
    })
    .then(response => response.json())
    .then(result => {
        load_posts(result)
    })
}


function load_posts(result){
    
    for (let i = 0; i < result["length"]; i++) {
        let header = document.createElement("a");
        let subheader = document.createElement("h5");
        header.class = "font-weight-light";
        let box = document.createElement("div");
        box.class = "border"
        let lineBreak = document.createElement("br");
        if (result[i][0].length >25){
            header.innerHTML = result[i][0].substring(0,result[i][0].length/2)
            header.append(lineBreak);
            header.innerHTML += result[i][0].substring(result[i][0].length/2)
        }
        else{
            header.innerHTML = result[i][0];
        }
        temp = result[i][0].toString()
        console.log(temp)
        let ns_title = temp.replace(/\s/g,"-")
        console.log(ns_title)
        header.href = `page/${ns_title}`;
        
        box.append(header);
        box.id = "post"
        subheader.innerHTML = result[i][2] + " " + result[i][1] + " " + result[i][3];
        box.append(subheader); 
        
     
        document.querySelector('#articles').append(box);
        

      } 
}


}) //dom content loaded ended 





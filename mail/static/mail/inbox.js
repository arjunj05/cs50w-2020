document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', submit_email);
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
    
  


}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`) 
  .then(response => response.json())
  .then(emails => {
    // Print emails
    emails.forEach(function(email){

      const div = document.createElement('div');
      div.id = 'email-id';
      div.style.borderStyle = 'solid'
      div.style.padding = '10px';
      if(email['read']){
        div.style.backgroundColor = 'gray';
      }
      else{
        div.style.backgroundColor = 'white';
      }

      const p1 = document.createElement('p');
      p1.style.float = 'left';
      p1.innerHTML = email['sender'] +   ":     "   + email['subject']

      const p2 = document.createElement('p');
      p2.style.textAlign = 'right'; 
      p2.innerHTML = email['timestamp'];

      div.append(p1);
      div.append(p2);
  
      div.addEventListener('click', () => load_email(email['id']));
      document.querySelector('#emails-view').append(div);

      

    })
  });


}

function submit_email(event){
  event.preventDefault()

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      load_mailbox('sent');
  });  

}

function load_email(id){

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(result =>{
    //update views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    document.querySelector('#email-view').innerHTML = '';

    //get parts of email
    const list = ["From: ", "To: ", "Subject: ", "Timestamp: "];
    const results = [result['sender'], result['recipients'], result['subject'], result['timestamp']];

    //add parts to a div
    const div = document.createElement('div');
    for(let i = 0; i<list.length; i++)
    {
      let bolded = document.createElement('b');
      bolded.innerHTML = list[i];
      div.append(bolded);
      div.append(results[i]);
      div.append(document.createElement('br'));
    } 
    div.append(document.createElement('br'));
    //div.append(result['body']);

    //adding div to view
    document.querySelector('#email-view').append(div);

    //archive feature
    archiveButton = document.createElement('button');
    archiveButton.setAttribute('class','btn btn-sm btn-outline-primary');
    if(result['archived'])
    {
      archiveButton.innerHTML = 'unarchive';
    }
    else{
      archiveButton.innerHTML = 'archive';
    }
    let x = !result['archived'];
    console.log(x);
    document.querySelector('#email-view').append(archiveButton);

    archiveButton.addEventListener('click', function(){
      
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: x
        })
      })
      .then(response => load_mailbox('inbox'))
    
    }) 

    //reply feature
    replyButton = document.createElement('button');
    replyButton.setAttribute('class','btn btn-sm btn-outline-primary');
    replyButton.innerHTML = 'Reply';
    document.querySelector('#email-view').append(replyButton);


    replyButton.addEventListener('click', function(){
      // Show compose view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#email-view').style.display = 'none';

      // Clear out composition fields
      document.querySelector('#compose-recipients').value = result['sender'];
      if(result['subject'].substring(0,3) === "Re:"){
        document.querySelector('#compose-subject').value = result['subject'];
      }
      else{
        document.querySelector('#compose-subject').value = `Re:${result['subject']}`;
      }
      document.querySelector('#compose-body').value = `On ${result['timestamp']} ${result['sender']} wrote: ${result['body']}`;

    })


    //adding body to view
    const div2 = document.createElement('div');
    div2.innerHTML = `<hr> ${result['body']} `;
    document.querySelector('#email-view').append(div2);


  })

  //marking as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  .then(response => response.json())
  .then(result =>{
    console.log('hello');
  }); 

    

}
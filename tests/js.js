//fetch('http://192.168.1.118:8000/delete-post-by-id/3', {
//  method: 'DELETE',
//})
//.then(response => {
//    console.log(".then")
//})
//.catch(error => {
//  console.error('Error occurred while making DELETE request:', error);
//});


//var xhr = new XMLHttpRequest();
//xhr.open("DELETE", "http://192.168.1.118:8000/delete-post-by-id/3", true);
//xhr.setRequestHeader("Content-Type", "application/json"); // Set appropriate headers if needed
//xhr.onreadystatechange = function () {
//    if (xhr.readyState === 4) { // Request completed
//        if (xhr.status >= 200 && xhr.status < 300) {
//            console.log("DELETE request successful");
//            // Handle response if needed
//        } else {
//            console.error("DELETE request failed with status:", xhr.status);
//            // Handle error
//        }
//    }
//};
//xhr.send(); // Send the request


//const fetch = require('node-fetch');

//fetch('http://127.0.0.1:8000/posts', {
//  method: 'GET',
//  mode: "cors", // no-cors, *cors, same-origin
//  cache: "no-cache",
//  headers: {
//    'Content-Type': 'application/json', // Set appropriate headers if needed
////    'Access-Control-Allow-Methods': "DELETE",
//    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
//    'Access-Control-Request-Method': "GET",
//    "Access-Control-Allow-Origin": "*",
//    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
//  },
//})
//.then(response => {
//  if (response.ok) {
//    console.log('DELETE request successful');
//    // Handle response if needed
//  } else {
//    console.error('DELETE request failed with status:', response.status);
//    // Handle error
//  }
//})
//.catch(error => {
//  console.error('Error occurred while making DELETE request:', error);
//});



//const axios = require('axios');
//
//axios.delete('http://192.168.1.118:8000/delete-post-by-id/4')
//  .then(response => {
//    console.log('DELETE request successful');
//    // Handle response if needed
//  })
//  .catch(error => {
//    console.error('Error occurred while making DELETE request:', error);
//  });


fetch('http://127.0.0.1:8000/delete-post-by-id/7')
  .then(response => {
    if (!response.ok) {
      console.log('Network response was not ok');
    }
    return response.status;
  })
  .then(data => {
    console.log('Data received:', data);
    // Do something with the received data
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });











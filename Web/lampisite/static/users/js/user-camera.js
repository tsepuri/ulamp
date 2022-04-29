(function() {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.

  var width = 320;    // We will scale the photo width to this
  var height = 0;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.
  var photos = []
  var username = ""
  var streaming = false;
  MAX_PHOTOS = 10
  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.
  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;

  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');

    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);
      
        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.
      
        if (isNaN(height)) {
          height = width / (4/3);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);

    startbutton.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
    }, false);
    
    clearphoto();
  }

  // Fill the photo with an indication that none has been
  // captured.

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }

  document.querySelector("#submit").addEventListener('click', (e) => {
    username = document.querySelector("#id_username").value
    if (username) {
      try {
        uploadPhotos()
      }
      catch (err) {
        console.log(err)
        document.querySelector(".warning").style.display = 'block'
      }
    }
  })
  document.querySelector("#max-photos").innerHTML = MAX_PHOTOS
   document.querySelector("#submit").style.display = 'none'
  document.querySelector(".warning").style.display = 'none'
  function uploadPhotos() {
    $.ajax({
        type: "POST",
        url: '/users/upload_photos',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            photos: JSON.stringify({
              photos}),
            username: document.querySelector("#id_username").value
        },
        dataType: "json",
        success: function (data) {
            // any process in data
            console.log("success")
        },
        failure: function () {
            console.log("failure");
        }
    });
  }
  
  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a PNG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.

  function takepicture() {
    console.log("Picture taken")
    var context = canvas.getContext('2d');
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);
      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
      photos.push(data)
      let currentPhotos = +document.querySelector("#num-photos").innerHTML
      if (currentPhotos == MAX_PHOTOS) {
        document.querySelector("#startbutton").style.display = 'none'
        document.querySelector("#submit").style.display = 'block'
        console.log("what now")
        console.log(photos)
      }
      else {
         document.querySelector("#num-photos").innerHTML = currentPhotos + 1
      }
    } else {
      clearphoto();
    }
  }

  // Set up our event listener to run the startup process
  // once loading is complete.
  window.addEventListener('load', startup, false);
})();
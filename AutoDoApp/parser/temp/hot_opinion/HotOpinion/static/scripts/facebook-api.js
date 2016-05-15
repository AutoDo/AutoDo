/**
 * Created by junojunho on 2015. 11. 22..
 */
// This is called with the results from from FB.getLoginStatus().
        function statusChangeCallback(response) {
            // The response object is returned with a status field that lets the
            // app know the current login status of the person.
            // Full docs on the response object can be found in the documentation
            // for FB.getLoginStatus().
            if (response.status === 'connected') {
              // Logged into your app and Facebook.
              testAPI();
            } else if (response.status === 'not_authorized') {
              // The person is logged into Facebook, but not your app.
//{#              document.getElementById('status').innerHTML = 'Please log ' +#}
//{#                'into this app.';#}
            } else {
              // The person is not logged into Facebook, so we're not sure if
              // they are logged into this app or not.
//{#              document.getElementById('status').innerHTML = 'Please log ' +#}
//{#                'into Facebook.';#}
            }
        }


        // This function is called when someone finishes with the Login
        // Button.  See the onlogin handler attached to it in the sample
        // code below.
        function checkLoginState() {
            FB.getLoginStatus(function(response) {
              statusChangeCallback(response);
            });
        }

        window.fbAsyncInit = function() {
            FB.init({
                appId      : '872475326201689',
                xfbml      : true,
                version    : 'v2.5'
            });

            checkLoginState();
        };

        (function(d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) return;
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/ko_KR/sdk.js#xfbml=1&version=v2.5&appId=872475326201689";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));

        function testAPI() {
            FB.api('/me', function(response) {
//{#                document.getElementById('status').innerHTML =#}
//{#                'Thanks for logging in, ' + response.name + '!';#}
            });
        }

Created HELM-BRANCH so nothing would be committed directly to Main. Pull Requests can be generated later to Merge. 

Created /tests/test-reports/ to house verbose output from Pytest in Pipeline 

Thoughts:

> My experience on the deployment of a Docker image helped accelerate the build of the dockerfile. 

> For all of the issues I ran into while running through the pipeline, given more time and more build hours, and with some familairity with ParlAI a bit more, 
I probably could have gotten some of the test python scripts fixed to the point where they could be ran. 

> I leaned on my research skills a lot for this experiment. I had to look up several things along the way but I feel confident with what I've produced here. 

Dilemmeas:

> For the dockerfile, I had the option of using a couple of different base images. Python really works well with Ubuntu, RHEL, or Debian, but I decided to go with the Docker Python 3.8 image 

Challenges: 

> Pipeline failed because memory overage for free tier of Bitbucket. 
Im going to try and restrict Pytest to less scripts just for the purposes of getting the pipeline to work. 

> Lint step keeps failing because provided ParlAI code is broken. 
I have tried multiple different test_.py files to no avail, they would need to be scrubbed and errors addressed. 

> I am running out of build time on the free tier of BitBucket so wrapping up pipeline development as I've used up a good bit of time troubleshooting.
I am comfortable with my pipeline configuration yml. It is very rudimentary. 
If this was a real project, I'd add in security checks (discovered a few different options here) to check the code for vulnerabilities, may need to work with DevSecOps if this is out of scope for my position),  
I would also add in more testing (Unit testing, browser testing). PyTest is at a very basic spot here just due to limitations.


Please reach out to me if you have any questions

Michael Goodeaux
michaelgoodeaux@gmail.com 
904 - 888 - 6212

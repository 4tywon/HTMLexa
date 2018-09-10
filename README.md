<img src="https://github.com/khou22/HTMLexa/raw/master/cover.png" />

## Introduction
*HTMLexa* is an Alexa Skill with a companion [web app](https://htmlexa.herokuapp.com/test) that allows people to build full-scale websites with his or her voice. We aimed to improve the accessibility of website creation through machine learning and a well-crafted user-experience spanning both the voice and digital spectrums.

## Inspiration
With the rise of technology and the resoluting Digital Divide, the Internet has become the underpinnings of modern communication. *Access* to information as well as *publishing* information is crutial to the success of a business, movement, or personal brand. We wanted to improve the accessibility of website creation by utilizing the power of Amazon Alexa.

With *HTMLexa*, the barrier for entry in creating websites has been drastically reduced. Voice commands provide ease of use to an entire new segment of the population including children, the blind, those without technological experience, the elderly, and many more. Website building — even drag and drop sites like Squarespace and Wix — are too complicated and time consuming for a vast majority of people. *HTMLexa* provides a painless way for people to creates online content — thereby instantly reaching millions of new people.

## What It Does
*HTMLexa* is an Alexa Skill that allows a user to dictate the creation of website. You can add titles, paragraphs, buttons, and even images to create a functional, powerful website with a modern look and feel. Here are a few examples:

1. "*Add a big image of of Princeton University*"
2. "*Move paragraph-1 into the left column below title-1*"
3. "*Add a banner with a beach background and the title, 'Welcome'*"


## How We Built It
In order to achieve the maximum level of continuity and flexiblity for different types of websites, we set out to create a design system of sorts. We started by creating mockups of common websites and picking out the most freqently used. Next, we decided which properties on each component would be user contributed. Finally, we created a collection of common elements that we would implement using ReactJS.

The Amazon Alexa functionality was built using Amazon's Alexa SDK. The scripting was done primary in AWS Lambda. We implemented our own database on AWS S3 because we didn't want to add the complexities of a PostGres or relational database.

The client app actually refers to both a frontend client and a server. Both the client and server are build using Webpack and served up using ExpressJS. The frontend is a React/Redux/Router stack with an ES6 and ExpressJS backend. The persist data is stored using Amazon S3 to allow for seamless data continuity across Lambda and the client.

## Challenges
We faced many challenges, in building this product. One of the major hurdles we faced was simply the engineering of code that writes other code. We essentially coded an app that would use machine learning write completely new code. This concept was at first difficult to design, but we soon were able to come up with a logical solution to this problem in the form of a dynamically compiled website.

We also encountered a handful of issues connecting various systems together. With everything from Amazon Alexa, Lambda, and S3 to Heroku, Python, and Webpack, our stack covered a wide variety of programming languages, systems, and designs. Getting the puzzle pieces to all fit together was a challenging, yet very rewarding problem to solve.

## Accomplishments That We're Proud Of
We are proud of the fact that we were able to tackle an immensly difficult challenge and come out with a polished, powerful, working product. While it is not perfect, given the 36 hour time period, we were able to accomplish quite a great deal. One of them ost interesting and rewarding experiences was building a user experience that spanned both voice and digital. It was an engaging adventure that provoked a lot of creativity and ingenuity.

## What We Learned
We learned an incredible amount about Amazon's Alexa as well as the design of large-scale systems. We also learned the principles of a unified component library and the benefits of building modular code.

## What's Next for HTMLexa
We are hoping to improve the client-side admin functionalities so that you can edit the site to a higher granularity using a web app platform. We're also hoping to add new components and features like multiple pages, templates, etc.

## Built With
Alexa Skills, AWS Lambda, Python, AWS S3, Heroku, NodeJS, React/Redux/Router, ExpressJS, and Webpack. The designs were done with Sketch.

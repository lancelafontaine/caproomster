# capRoomster 

## File Structure

```
- /application
-----+ /component
----------+ component.module.js
----------+ component.controller.js
----------+ component.template.html
----------+ component.scss
----------+ component.component.js
----------+ component.config.js
----------+ component.service.js
----------+ component.factory.js
----------+ component.model.js
-----+ capRoomster.module.js
-----+ capRoomster.config.js
-----+ capRoomster.scss
-----+ index.html
- /test
-----+ test.comfig.js
-----+ component
----------+ component.component.test.js
----------+ component.controller.test.js
----------+ component.service.test.js
----------+ component.factory.test.js
- bower.json
- gulpfile.js
- package.json
- README.md
```

## Developing Commands

### Project Setup

- `npm run setup` to set up the project
- `npm run reset` to reset the project

### Build Application

- `npm run package` to build the web application into `dist` folder

### Development

- `npm run package` to package the application into `dist` folder
- `npm run clean` to delete build folders
- `npm run start` to run the application on Chrome
- `npm run test` to run unit tests

## Documentation Reference

- [AngularJS Guide](https://docs.angularjs.org/guide)
- [AngularJS API Documentation](https://docs.angularjs.org/api)

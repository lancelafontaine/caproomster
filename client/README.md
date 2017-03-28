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
- bower.json
- gulpfile.js
- package.json
- README.md
```

## Developing Commands

### Project Setup

- `npm install` to set up the project
- `npm run uninstall` to reset the project

### Build Application

- `npm run pack` to build the web application into `dist` folder

### Development

- `npm run pack` to package the application into `dist` folder
- `npm run clean` to delete build folders
- `npm run start` to run the application on a web browser, on localhost:8080
- `npm run check` to check syntax and format error
- `npm run check:fix` to automatically fix syntax error

## Documentation Reference

- [AngularJS Guide](https://docs.angularjs.org/guide)
- [AngularJS API Documentation](https://docs.angularjs.org/api)

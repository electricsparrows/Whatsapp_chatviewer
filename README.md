# Chat History Viewer

**What it is:**
- a management application which allows you to load in exported
WhatsApp chat history files, to browse and manage your messages more conveniently.
  

- [ ] Allows you to look for a message on a given date,
  so that you don't have to scroll through the whole log. 
  
- [ ] Allows you to tag a message to save for later

- [ ] Allows you to add annotated comments to a message.

- [ ] Provides a visualization of chat activity over time.

- [ ] Keyword search

### DESCOPED features:
- [ ] reconcile duplicate messages on import
- [ ] Provide a noun summary of a set messages -- 
  so that we can see topics discussed in a set of messages, without actually having to read their contents.


------------------------------------------------
### Things to do:
- [ ] need to update time parsing function to support seconds.

- [ ] user input validation functions:
      - enter file path
      - enter date str
      - enter search keyword

- [ ] using PugSQL may have been a good idea, they return results as dictionaries

- [ ] connect database functions with the controller functions

- [x] implement `yoy_activity`

- [ ] implement `retrieve by keyword`

- [ ] fix the parsing of speaker_name issue
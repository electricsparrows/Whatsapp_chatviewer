# Chat History Viewer

**What it is:**
- a management application which allows you to load in exported
WhatsApp chat history files, to browse and manage your messages more conveniently.
  
- [x] Allows you to look for a message on a given date,
  so that you don't have to scroll through the whole log. 
  
- [x] Allows you to tag a message to save for later

- [x] Allows you to add annotated comments to a message.

- [ ] Provides a visualization of chat activity over time.

- [x] Keyword search

- [x] reconcile duplicate messages on import

### DESCOPED features:

- [ ] Provide a noun summary of a set messages -- 
  gives a brief overview of topics discussed in a set of messages, 
  without actually having to read their contents.


------------------------------------------------
### Things to do:
- [x] connect database functions with the controller functions
- [x] implement `yoy_activity`
- [x] implement `retrieve by keyword`
- [x] need to update time parsing function to support various timestamps
- [x] fix the parsing of speaker_name issue
- [x] add the import_ref during parse()
- [x] import ref --
    - generate a unique session ref. no before parsing
    - import all associated tuples with that code

- [ ] complete unit tests in test_filehandler

- [x] build gui components
    - [ ] display notes component
      [ ] edit/ add msg note component
    - [ ] add tag component
    - [ ] view tags component
    - [ ] implement conversation list
    - [ ] activity heatmap/ chart
    
- [x] test file import
    - [x] still has issues with reconciling duplicate records
    - [x] convo head indicator -- algorithm done
        
- [x] user input validation functions:
      - [x] enter file path (restrict in gui component)
      - [x] enter date str (use isoformat everywhere)
      - [x] enter search keyword






# CHANGELOG



## v1.1.0 (2024-02-15)

### Chore

* chore: remove auto created CHANGELOG.md ([`6572e44`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6572e44b0830442f2c834e71341635db55a84471))

* chore: add configuration to publishes artefacts to GitHub Releases ([`dcc28fd`](https://github.com/N5GEH/n5geh.tools.entirety/commit/dcc28fde35da858382d4c3eb97516218ab464fc6))

* chore: remove extra files created by semantic release ([`3645371`](https://github.com/N5GEH/n5geh.tools.entirety/commit/36453710a359bd855e55feb294f1053e5172cfa9))

* chore: adjust pydantic version ([`80375df`](https://github.com/N5GEH/n5geh.tools.entirety/commit/80375df7dad51044bdc3eb75f43c0e2346615db4))

* chore: adapt view only role in subscription app ([`45a175f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/45a175f4bdf7ad8fe6e8ce0edd220a177c4424da))

* chore: adapt view only role in devices app inspect view ([`4e606b7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4e606b78764ec1fe0d318a63f412ff7b209d36d5))

* chore: adapt view only role in devices app ([`10bbad0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/10bbad0c8ea3cecac1b1ccea9cbe1fa03084a4a0))

* chore: delete not reachable code block ([`9f5e7f3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9f5e7f332347cc3f88663020f81b0a37589b543e))

* chore: handel multiple selection in entity list ([`46bc8e6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/46bc8e66dadb42978754bf3e63e791f2c185f965))

* chore: replace deprecated substr() ([`66f8159`](https://github.com/N5GEH/n5geh.tools.entirety/commit/66f8159a71760a58d33f8cea5b0458ad9e3008ff))

* chore: include support for CSRF_TRUSTED_ORIGINS (#129) ([`cdd441e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cdd441e49425d54031651016609eb102371bdb8e))

* chore: update Pillow version to 9.3.0 (#141) ([`82d029f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/82d029f079df1dcd0f57c17fd0ae51015b6aa94c))

* chore: base semantics app (#105)

* chore: base semantics app

* Layout semantics app

* safety

* Add detail-level

* add sementics views

* update configurations (.env docker-compose)

* Start working on Fiware communication

* Finished communication with Fiware and added comments

Now the entities will be queried from the context broker and then loaded into the visualisation

* graph zoom limitation

* Show entity

* Integration of entity Tabel

-integration of he entity tabel. No Styling, still default layout

* Adding of several features

-&gt; finishing and styling of entity Table
-&gt; Add Dropdown menu for Legend in main graph
-&gt;Start working on Search feature

* Bugfix: fix deatail-level

* Nodes coloring, legend adjustment

relationship coloring will follow

* Nodes coloring, legend adjustment

edge coloring will follow

* Selection of different labels

* Bug fix: node coloring

Nodes return to default color when checkbox is unchecked

* Bug fix: new docker volumes created with every restart (Windows)

Before pulling: docker-compose down
After pulling: superuser &amp; project must be recreated (with old data)

* parents and children highlighting

* Edge coloring

* legend: stack order fixed

* fixed: cursor stays default when hovering over text in dropdown

* Enables Layout selection

* Click to view next entity (table and detail level)

* Adjustment of color scheme

* info for presentation

* Enable search, edit Buton, layout entity table, start coloring

* Added new Features

* Fixed scrolling and Bugfixing

* display warning longer

* implementation of review changes

* deleted unused file, placed cytoscape.umd.js and tabulator.min.js in seperate folders under /static

* Delete app/Entirety/docker-compose.yml

file is only necessary in the step-by-step

---------

Co-authored-by: Johannes Radebold &lt;johannes.radebold@rwth-aachen.de&gt;
Co-authored-by: Hanna Hesel &lt;hanna.hesel@eonerc.rwth-aachen.de&gt;
Co-authored-by: Sebastian Blechmann &lt;51322874+SBlechmann@users.noreply.github.com&gt; ([`f2cb4b6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f2cb4b6950d780ad2b5eadb7b6e302e4ce92eb67))

### Documentation

* docs: update roadmap ([`45327b3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/45327b3d02d5e91fc9bec57da6f790110da861b8))

* docs: update roadmap ([`b596478`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b596478fe9bc8162bc03e1b4e1c4b0d95633dbda))

### Feature

* feat: addition of new viewer role with corresponding changes in Entity App ([`d3bbd45`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d3bbd45ccdbd93be2474f7756a9b750be4f1fd52))

* feat: disable project admin (maintainer) to update fiware service and to create new project ([`efb753c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/efb753c0fdb1faa4113b360c3cdcda4ada8a8759))

* feat: disable project admin (maintainer) to update fiware service and to create new project ([`487b0b1`](https://github.com/N5GEH/n5geh.tools.entirety/commit/487b0b164a86e5d628d4b1137002d6a2a503ec41))

### Fix

* fix: rework semantic release ([`3ed8e89`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3ed8e8955be2ff3c4d1e3af3a966a92555061677))

* fix: local auth admin site can not create users ([`528f194`](https://github.com/N5GEH/n5geh.tools.entirety/commit/528f194a7955b117d93e94772eeeb801c9708517))

### Refactor

* refactor: restrict post methods from viewer role ([`ea039a9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ea039a915d9ebafcd15b1538afb0616148074e01))

* refactor: adapt view only role in subscription app ([`cceec47`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cceec474c986df7b7fd96a14bddc4b4134c0f753))

* refactor: change label edit to inspect in entity app ([`1336226`](https://github.com/N5GEH/n5geh.tools.entirety/commit/133622626e9cd50ff4bc6f3919b33c99f9c05ac2))

* refactor: remove redundant parenthesis ([`1253158`](https://github.com/N5GEH/n5geh.tools.entirety/commit/12531584fe7abb08fe43407394d2cf549cc5bfe2))

### Unknown

* Merge branch &#39;163-refactor-semantic-release&#39; ([`2f711bb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/2f711bbbc27208c624f08e7fef7d546ca3fcb915))

* 1.1.0

Automatically generated by python-semantic-release ([`7e21021`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7e21021012508d5345000d7787540c0696c4acda))

* 1.1.0

Automatically generated by python-semantic-release ([`1e60dc9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1e60dc993a28d1e60483b7c130bbafffa94dd702))

* Merge pull request #162 from N5GEH/development

new release 2024-02-07 ([`a93dbab`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a93dbab930be1bc54d8fb539437ef874d7a08ba2))

* Merge pull request #161 from N5GEH/160-release-preparation

160 release preparation ([`fa6e582`](https://github.com/N5GEH/n5geh.tools.entirety/commit/fa6e582ae055e6410eeb9a56f5819623d4703b1c))

* Merge branch &#39;main&#39; into 160-release-preparation ([`5be56ed`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5be56edaa1ca43279aea133b7a16e2f4b89cb82b))

* Merge pull request #153 from N5GEH/147-add-viewer-role-in-app

add viewer role ([`d8f3acd`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d8f3acd04ade0f0d7c589996d348f6e83b9cc9d8))

* Merge pull request #157 from N5GEH/156-pydantic-version-error

fix pydantic version error ([`31f8687`](https://github.com/N5GEH/n5geh.tools.entirety/commit/31f86878cde3a4e75aab223568ab64884f35e8e0))

* Update requirements.txt ([`befaa3c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/befaa3c087d056950c7309d597cb264024c7b3c8))

* Merge pull request #140 from N5GEH/138-disable-update-to-fiware-service-for-project-admins

138 disable update to fiware service for project admins ([`f02af4d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f02af4d20643a5110ff1d1b873b9738bdbef2d58))

* Merge pull request #145 from N5GEH/142-update-semantics-app

142 update semantics app ([`1fef1a7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1fef1a740a5028b8200653f6b0248964691b3903))

* Merge remote-tracking branch &#39;origin/142-update-semantics-app&#39; into 142-update-semantics-app ([`48ecd06`](https://github.com/N5GEH/n5geh.tools.entirety/commit/48ecd06e619f7bfa39c49f655d04b79e1d7d4885))

* Merge remote-tracking branch &#39;origin/142-update-semantics-app&#39; into 142-update-semantics-app ([`294e789`](https://github.com/N5GEH/n5geh.tools.entirety/commit/294e789f970c7987237129fd62af4df00d943817))

* review changes ([`3201367`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3201367a06f5fd353d44090c846e22bae7948e3d))

* Merge preparations ([`07ecf14`](https://github.com/N5GEH/n5geh.tools.entirety/commit/07ecf14a4feac0b90129b44ae051358c5b369bf0))

* Finished autocomplete search ([`63edb8b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/63edb8bc83dc4c78df300850c1326c436b3bf3e3))

* Automated data collections for types in autocompletion, bugfix start search on enter ([`f65d223`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f65d2235fcda487d74eb79604b2b7b6ed031d24c))

* First Version of autofill ([`c670690`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c67069021456b3f788eeb4c97cd7a29abf1c3a1f))

* Merge branch &#39;cake-cxtmenu&#39; into 142-update-semantics-app

# Conflicts:
#	app/Entirety/semantics/templates/semantics/semantics_visualize.html
#	app/Entirety/static/js/semantics.js
#	app/Entirety/static/semantics/css/base.scss ([`52a732e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/52a732ec2cf4791d18ea500df9e61beb93991b14))

* deleted unused file, placed cytoscape.umd.js and tabulator.min.js in seperate folders under /static ([`fc5b587`](https://github.com/N5GEH/n5geh.tools.entirety/commit/fc5b587b22657336f25bc8d26a2ea3282a1edadb))

* merge preparation ([`601ced5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/601ced528dc17127d38ac04624be120dfe0f1504))

* design fixes ([`279c2ce`](https://github.com/N5GEH/n5geh.tools.entirety/commit/279c2cefa4d60ebbeb4855d09bfa7393539a3c4f))

* Implement funding information (#71)

* Create PR for #70

* docs: implemented funding information and project link

---------

Co-authored-by: SBlechmann &lt;SBlechmann@users.noreply.github.com&gt;
Co-authored-by: Sebastian Blechmann &lt;sebastian.blechmann@eonerc.rwth-aachen.de&gt; ([`c3bed82`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c3bed82f9d23ba3a519472b3dad372edfca73126))


## v1.0.0 (2023-09-05)

### Breaking

* chore: change database environment variables

BREAKING CHANGE: the env variable DATABASE_URL is now split into DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, and DATABASE_HOST ([`ac6f84f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ac6f84fdda6ed25435812e45b5c01f7ad25bf60f))

### Chore

* chore: update token ([`5de2199`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5de2199c2f2f0948cbdc8815336e8fe20ba4aa35))

* chore: update token ([`6a74a53`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6a74a539f9c9d5d2ae3d59308b3090256d59bf74))

* chore: update devices app roadmap ([`b327d51`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b327d51fc051d61f7ee795077c3fe7f2c8f7ce59))

* chore: limit column length for entity and service group ([`b2d3e03`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b2d3e03290547bbea6b1383d7b6c7d806fbaec21))

* chore: adaption of ROADMAP.md ([`2c831d2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/2c831d2ecf77c35fc283fef2845d9c89932d974e))

* chore: change image build back to main and development ([`b228f9e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b228f9e94c8ccbc2b5f21bf03c0d3bfd090744cf))

* chore: test image ([`deacc83`](https://github.com/N5GEH/n5geh.tools.entirety/commit/deacc8382ce9264141b21bb31700945ba23c6b1b))

* chore: create image for this branch ([`0a3a7f5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0a3a7f59f01e539dc662057a132dd93c305bdf2a))

* chore: temporary change to solve the pydantic issue ([`4a20a09`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4a20a09f4c3ebbf283e304f6b8a946c16392d958))

* chore: create default super user ([`4d84f22`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4d84f22b0d79151d03dabfaee11b2de1e176cf4a))

* chore: default search by id ([`a2d370f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a2d370f7733d9214a201f185442497cea13fda9d))

* chore: single button for searching entities ([`3ed1af9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3ed1af9af199568f781d7fd36d56c329fb522e43))

* chore: update docs ([`5fb6aaf`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5fb6aafacd324b00f143d3a898dd98e09e1cffbc))

* chore: handle other attribute types (#101)

* chore: handle other attribute types

* fix: move common entirety list text widget

* chore: change attribute type to charfield in devices app

* fix: error while merging

* chore: update filip version

* chore: disable type validator of get_attributes

---------

Co-authored-by: JunsongDu &lt;junsong.du@eonerc.rwth-aachen.de&gt; ([`7659835`](https://github.com/N5GEH/n5geh.tools.entirety/commit/765983576b72137cfc9b656f4666b2c81e7e3a1c))

* chore: update roadmap ([`9dced89`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9dced89ef294f29e6671f6891c125c0e4b1fc2e2))

* chore: add error logger for devices app ([`89db589`](https://github.com/N5GEH/n5geh.tools.entirety/commit/89db589dca58b0bb7a2735392af0527cd2bd4bc5))

* chore: merged dev into current ([`9a6c345`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9a6c3457902fb309973edc51169628b34562b9df))

* chore: merged dev into current ([`9ad4f12`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9ad4f127849594015e78632067785f1bd02c0e58))

* chore: remove extra code ([`ac7b12c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ac7b12c275047fc57448d41c9d5425c2a5b9fa5c))

* chore: tiny adjustment ([`ea0e3ec`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ea0e3ec7a2f6d4fa26dcd7d150a7653adb7f4565))

* chore: move group form to separate script ([`9fb5771`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9fb577146bb7b9c6784ec8776c4f2d6e60fc69c5))

* chore: move group form to separate script and add tooltips ([`4f02317`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4f02317382670299bf8717c781a548bc55d0934b))

* chore: base semantics app ([`ebfb75e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ebfb75ebee08e1fb74ed283f17b0afc81b2ab031))

* chore: basic logging for subscriptions app ([`ed8a237`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ed8a237920208da3696aa728d80e5bd80e2a09fd))

* chore: made common utils function for session data ([`c263c3e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c263c3e88355f29a2b79d555337df7b15cd225d3))

* chore: delete session data after usage ([`4aa148e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4aa148ef352cee15369d1cddad3ba08f15210895))

* chore: disable other existing loggers ([`05b4376`](https://github.com/N5GEH/n5geh.tools.entirety/commit/05b437670fe6ea0bf09e62c260013b1a4ee61023))

* chore: add more info to logger ([`6d7512e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6d7512ef6d5bd29217febe61423e5b7f67cabf32))

* chore: add logger for devices app ([`f7b919d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f7b919daa6c1e02daed6c6d235f7c5fe3c022f4e))

* chore: added entities logging ([`15d7093`](https://github.com/N5GEH/n5geh.tools.entirety/commit/15d7093eef3f6c86e810b7d9cd9e23aa913511fb))

* chore: added oidc basic logging ([`89eea82`](https://github.com/N5GEH/n5geh.tools.entirety/commit/89eea82d60de2dc70bae20b8d4f9a676059cdb84))

* chore: segregate loki and console logging ([`9608341`](https://github.com/N5GEH/n5geh.tools.entirety/commit/96083417d0bd63ce61d5112e1a2d7b188d44c4c8))

* chore: increase trigger interval (#88) ([`952eb8c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/952eb8ceea2dfc464d78577043f39aca4bb9c56f))

* chore: fiware service exception from filip (#86) ([`a899f93`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a899f93deebc5c447ee5bc2a9deba32bbf0df9c0))

* chore: disable editing resource and apikey ([`0ee2ac2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0ee2ac2c3f2c3283aae77bbe99797fc8bdf34f0b))

* chore: change default value of boolean params ([`e245693`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e245693d4cf271ff7cb2cdb72247a749323547dd))

* chore: service groups list view ([`623fd7e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/623fd7e018b471cacaed64a3f2b86cc412c9698c))

* chore: first draft of tabs ([`abe34d2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/abe34d2373215eb2c29706c826c8795a53d43e6c))

* chore: add bootstrap icons as vendored ([`cf0eb27`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cf0eb27dd37427d311999413bb3250c6ee9e8269))

* chore: remove automatic branch creation

Use GitHub native feature for future branch and pull request creation ([`6eee91d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6eee91d4cabda815c8cd84f1f5eb6b6de280de98))

### Documentation

* docs(fix): fixed typo ([`20fb7ce`](https://github.com/N5GEH/n5geh.tools.entirety/commit/20fb7ceff002d219bbeb8563e7acf46629a153fb))

* docs: update setup guide (#73)

* Create PR for #72

* chore: update compose reference

* docs: update deployment guide

* fix: cleanup requirements

* docs: update deployment guide

* docs: moved deployment guide to separate repository

* fix: fixed superuser creation

* chore: fix typo

Co-authored-by: dnikolay-ebc &lt;dnikolay-ebc@users.noreply.github.com&gt;
Co-authored-by: dnikolay-ebc &lt;daniel.nikolay@rwth-aachen.de&gt; ([`8a7bf65`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8a7bf652430ca1c379a05406c42f4beeb1bf81b0))

* docs: update docs ([`517bd4e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/517bd4ea5b750e82f15e081405ea789549f4c584))

### Feature

* feat: add length limitation for columns in table ([`3d6b189`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3d6b1894270dbfa4676136fb991b673fcf04ade1))

* feat: allow batch devices creation from json payload ([`f989e84`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f989e84499fc2ebdf2cd762ab92cb0521a60dcdb))

* feat: batch deletion for devices and service groups ([`1e55a4d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1e55a4d38da3e41596f1cde29db1773821dd5cef))

* feat: show the device if duplicated ([`58d9a88`](https://github.com/N5GEH/n5geh.tools.entirety/commit/58d9a8844ad816b78edc1e2f0e6ccba4064e84c6))

* feat: add logger for service group CRUD ([`2852282`](https://github.com/N5GEH/n5geh.tools.entirety/commit/285228229c091183c77cc772a9edea39a5500f12))

* feat: implement filter for service groups ([`7a17af2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7a17af2839a61d40d390a023f2ec7e0a4f26fba0))

* feat: redirection of service group tab ([`74d82ac`](https://github.com/N5GEH/n5geh.tools.entirety/commit/74d82ac32a89f6e03edeb0aaee94b2d9bf2b2a0f))

* feat: service group curl option ([`8b82f25`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8b82f25a80ebc92442c803cb30fbfa6e90631f68))

### Fix

* fix: json.js conflict ([`3ea292e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3ea292e37b4a0bf9d4311285f41a6249e85bbebb))

* fix: it should be search-entity in the html ([`97ab821`](https://github.com/N5GEH/n5geh.tools.entirety/commit/97ab82171a6a2e866fdff445a096dc1f5bc5b254))

* fix: explicit_attrs instead of explicitAttrs ([`4f3fd69`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4f3fd69956b38127e79f5608ba59e70988b37bc8))

* fix: checkbox bugs ([`5704c80`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5704c80ad390f22345965ad285fe2899385a183a))

* fix: fixed consistency in subscription deletion (#102) ([`a25f325`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a25f32541c48c5b64dcbb37d294dcf165aad7b76))

* fix: typo ([`bf50666`](https://github.com/N5GEH/n5geh.tools.entirety/commit/bf506667a400113d1c58dc03b66d110ad4104351))

* fix: fixed enabler type ([`052ebd0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/052ebd0196f0ecb0e953ca52177a46da3e32e076))

* fix: delete related devices ([`9e3a067`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9e3a06711ffbe1ec3e709e0a2a84d8049ce48547))

* fix: add error handling ([`bc551a6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/bc551a639f70c0392f1c23e62db20e1fbb75f465))

* fix: both project and server admin in owner dropdown ([`76df880`](https://github.com/N5GEH/n5geh.tools.entirety/commit/76df88093d0337076e261f8338a43b150eb56d6b))

* fix: optimize settings (#77)

* Create PR for #76

* chore: optimize object creation

* chore: app load by default

Co-authored-by: sbanoeon &lt;sbanoeon@users.noreply.github.com&gt;
Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt; ([`de9d7e7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/de9d7e706c6f2a254c99692cd872086528edc8e5))

* fix: update frontend frameworks (#61) ([`220f26c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/220f26c02017853f5943bb8baed3275b4ea6f7ad))

* fix: prevent storing password hashes for oidc auth ([`a8fe241`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a8fe24195cb281afc8f706c7220aba02eeb1036a))

### Unknown

* 1.0.0

Automatically generated by python-semantic-release ([`15979e2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/15979e2592bb1876fe78feee7c81a1ebc2f8d764))

* Merge pull request #135 from N5GEH/133-token-for-semantic-release-outdated

chore: update token ([`c9d80c5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c9d80c57d0a6d0b616ed1ed85f96da56ee8d2fa5))

* Merge pull request #134 from N5GEH/133-token-for-semantic-release-outdated

chore: update token ([`f6e88ea`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f6e88eab632c231a151b2cfb6b116cb5a408dc9c))

* Merge pull request #132 from N5GEH/development

New release ([`e827c42`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e827c421ab89f1adb777ea38e0d6dfd563f38524))

* Merge pull request #131 from N5GEH/revert-128-development

Revert &#34;new release&#34; ([`fabdab5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/fabdab584cccbf1f4d40d813d919e87cba2ff57f))

* Revert &#34;new release (#128)&#34;

This reverts commit a4d783b527a7f2caa7608fb414537f3c2a88c266. ([`e093f20`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e093f205ebca0d1d483515bf54008505f89d2b4a))

* new release (#128)

* Create PR for #68

* docs: update docs

* Create PR for #74

* fix: prevent storing password hashes for oidc auth

* Create PR for #78

* docs: update setup guide (#73)

* Create PR for #72

* chore: update compose reference

* docs: update deployment guide

* fix: cleanup requirements

* docs: update deployment guide

* docs: moved deployment guide to separate repository

* fix: fixed superuser creation

* chore: fix typo

Co-authored-by: dnikolay-ebc &lt;dnikolay-ebc@users.noreply.github.com&gt;
Co-authored-by: dnikolay-ebc &lt;daniel.nikolay@rwth-aachen.de&gt;

* fix: update frontend frameworks (#61)

* fix: optimize settings (#77)

* Create PR for #76

* chore: optimize object creation

* chore: app load by default

Co-authored-by: sbanoeon &lt;sbanoeon@users.noreply.github.com&gt;
Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt;

* chore: remove automatic branch creation

Use GitHub native feature for future branch and pull request creation

* chore: add bootstrap icons as vendored

* chore: first draft of tabs

* WEB_URL missing in settings doc (#83)

* Create PR for #82

* docs(fix): web_url to web_host

Co-authored-by: sbanoeon &lt;sbanoeon@users.noreply.github.com&gt;
Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt;

* add users to project (#63)

* Create PR for #62

* fix: static root for collection

* chore: added users to project option

* chore: enable owner change for server admin

* fix: manual created superuser dose not have superuser access

* fix: project admin should not see all projects

* fix: owner field optional for non-server admins

* fix: project admin limited update options

Co-authored-by: sbanoeon &lt;sbanoeon@users.noreply.github.com&gt;
Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt;
Co-authored-by: JunsongDu &lt;junsong.du@eonerc.rwth-aachen.de&gt;
Co-authored-by: Saira Bano &lt;79838286+sbanoeon@users.noreply.github.com&gt;

* chore: service groups list view

* feat: service group curl option

* feat: redirection of service group tab

* chore: change default value of boolean params

* chore: disable editing resource and apikey

* chore: fiware service exception from filip (#86)

* chore: increase trigger interval (#88)

* fix: both project and server admin in owner dropdown

* chore: segregate loki and console logging

* fix: add error handling

* fix: delete related devices

* chore: added oidc basic logging

* chore: added entities logging

* fix: fixed enabler type

* 90 batch crud entities (#94)

* chore: batch create entity from json

* fix: used filip update function instead of post

* chore: delete batch entities

* chore: force delete entities

* chore: include json icon

* chore: include example in form

* chore: exception handling in list view

* fix: typo

* feat: implement filter for service groups

* chore: add logger for devices app

* chore: add more info to logger

* chore: disable other existing loggers

* chore: delete session data after usage

* 95 update contribution guidelines (#96)

* docs: GitHub workflow for development

* docs(fix): docker image

* fix: addition according to review

* fix: fixed consistency in subscription deletion (#102)

* chore: made common utils function for session data

* chore: basic logging for subscriptions app

* chore: move group form to separate script and add tooltips

* chore: move group form to separate script

* chore: tiny adjustment

* fix: checkbox bugs

* chore: remove extra code

* fix: explicit_attrs instead of explicitAttrs

* chore: merged dev into current

* feat: add logger for service group CRUD

* chore: add error logger for devices app

* chore: update roadmap

* docs(fix): fixed typo

* 107 include new user flags for user roles (#111)

* chore: include maintainer flag for projects

* chore: update option for maintainer on sidebar

* chore: include widget

* chore: include maintainers in project context

* fix: fixed maintainer function

* chore: handle other attribute types (#101)

* chore: handle other attribute types

* fix: move common entirety list text widget

* chore: change attribute type to charfield in devices app

* fix: error while merging

* chore: update filip version

* chore: disable type validator of get_attributes

---------

Co-authored-by: JunsongDu &lt;junsong.du@eonerc.rwth-aachen.de&gt;

* chore: change database environment variables

BREAKING CHANGE: the env variable DATABASE_URL is now split into DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, and DATABASE_HOST

* chore: update docs

* feat: show the device if duplicated

* feat: batch deletion for devices and service groups

* 84 user experience improvement (#100)

* Add entirety logo to banner

* Make website and logo optional in new project form

* Add dropdown for entities in subscription form

* Add entirety logo to banner

* Make website and logo optional in new project form

* Add dropdown for entities in subscription form

* Add multi value field for entity/type pattern and id

* Move subscription create/update button to bottom of form
Change style to match entity create button

* chore: re-arrange logo

* chore: use blank image as default

* chore: change tooltip to dynamic

---------

Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt;
Co-authored-by: JunsongDu &lt;junsong.du@eonerc.rwth-aachen.de&gt;

* chore: single button for searching entities

* fix: it should be search-entity in the html

* chore: default search by id

* chore: create default super user

* chore: temporary change to solve the pydantic issue

* chore: create image for this branch

* chore: test image

* chore: change image build back to main and development

* 99 display metadata in entities app (#118)

* chore: handle metadata in entity form

* chore: tooltip for metadata

* fix: fixed tooltip key title in javascript

* fix: change method to load json from string and not a file

* fix: error handling for metadata in Create and Update

* chore: adaption of ROADMAP.md

* feat: allow batch devices creation from json payload

* feat: add length limitation for columns in table

* chore: limit column length for entity and service group

* fix: json.js conflict

* chore: update devices app roadmap

---------

Co-authored-by: Daniel Nikolay &lt;88837885+dnikolay-ebc@users.noreply.github.com&gt;
Co-authored-by: dnikolay-ebc &lt;dnikolay-ebc@users.noreply.github.com&gt;
Co-authored-by: dnikolay-ebc &lt;daniel.nikolay@rwth-aachen.de&gt;
Co-authored-by: djs0109 &lt;djs0109@users.noreply.github.com&gt;
Co-authored-by: github-actions[bot] &lt;41898282+github-actions[bot]@users.noreply.github.com&gt;
Co-authored-by: sbanoeon &lt;sbanoeon@users.noreply.github.com&gt;
Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt;
Co-authored-by: Saira Bano &lt;79838286+sbanoeon@users.noreply.github.com&gt;
Co-authored-by: richardmarston &lt;mail@richardmarston.net&gt;
Co-authored-by: Sebastian Blechmann &lt;sebastian.blechmann@eonerc.rwth-aachen.de&gt; ([`a4d783b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a4d783b527a7f2caa7608fb414537f3c2a88c266))

* Merge pull request #116 from N5GEH/115-batch-operation-of-devices

Batch operation of devices ([`1b89182`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1b891821b0c196d8b6b16db9a05278203f27abe7))

* Merge pull request #109 from N5GEH/108-update-roadmap

chore: update roadmap ([`88043f0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/88043f0b0e3732e2db511593ec6d6603fb54d06e))

* Frontend fixes

- search bar (semantics, entities), overall design fixed and &#34;enter=search&#34; added
- button: restore entities list (entities)
- arrows: switch between views (semantics)
- beautified nested attrs in entity table (semantics)
- scrollbar issue fixed (semantics) ([`caf1354`](https://github.com/N5GEH/n5geh.tools.entirety/commit/caf13542389aab5b180568c6aa9ab7ead5be73eb))

* Merge branch &#39;development&#39; into 115-batch-operation-of-devices

# Conflicts:
#	app/Entirety/static/js/json.js ([`4aeb6a3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4aeb6a3dd4df3b98a94488ac5a864c9b92ab9e5e))

* 99 display metadata in entities app (#118)

* chore: handle metadata in entity form

* chore: tooltip for metadata

* fix: fixed tooltip key title in javascript

* fix: change method to load json from string and not a file

* fix: error handling for metadata in Create and Update ([`d693839`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d6938390e125c308f093aacf72d44faa5ec2c8b5))

* Merge pull request #126 from N5GEH/125-rework-entirety-image

125 rework entirety image ([`9980475`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9980475591fca98921cb1a92e1b4f0e810be5fe8))

* fix handleClick ([`6e3a521`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6e3a52181a02a724fd9431cd21fef3295acd7eea))

* Contextmenu added, design fixes ([`ec9cce7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ec9cce7f2d24a05458c370c038032c56d1a2c4b3))

* implementation of review changes ([`27ce67f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/27ce67fd09fbaffecef19fa910813d7bc19353b7))

* Merge branch &#39;development&#39; into 104-integrate-semantics-app ([`fbc0193`](https://github.com/N5GEH/n5geh.tools.entirety/commit/fbc01935c6bea7c1595e5a0e3ce633bd29a509eb))

* Merge pull request #120 from N5GEH/119-change-search-bar-in-entity-app

chore: single button for searching entities ([`024710c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/024710c23bb01c18dde436f76d3badecb06216f6))

* display warning longer ([`49e65e6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/49e65e6ecca18d24b3cac22932e36f26ddaf199f))

* 84 user experience improvement (#100)

* Add entirety logo to banner

* Make website and logo optional in new project form

* Add dropdown for entities in subscription form

* Add entirety logo to banner

* Make website and logo optional in new project form

* Add dropdown for entities in subscription form

* Add multi value field for entity/type pattern and id

* Move subscription create/update button to bottom of form
Change style to match entity create button

* chore: re-arrange logo

* chore: use blank image as default

* chore: change tooltip to dynamic

---------

Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt;
Co-authored-by: JunsongDu &lt;junsong.du@eonerc.rwth-aachen.de&gt; ([`b934018`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b93401873284bcfee3392ae78a8e4240112d87f3))

* Fixed scrolling and Bugfixing ([`9033f1c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9033f1cafda9adb04da886e912e94da40934655c))

* Added new Features ([`d6bac4a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d6bac4adc55ac073adce66e3da5bfc9e073a5512))

* Enable search, edit Buton, layout entity table, start coloring ([`76f7bb9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/76f7bb92d8e0f85a8c9d04c6fccc45f2eb8ef59c))

* info for presentation ([`357bf90`](https://github.com/N5GEH/n5geh.tools.entirety/commit/357bf905f9db3835ff439a1ece17138d1e2d017d))

* Adjustment of color scheme ([`e4d904e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e4d904e65fbc6e6350d52f6706c67cc33dc364de))

* Click to view next entity (table and detail level) ([`1fc2e93`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1fc2e9335397ead552cc7c9d475ee42936018f07))

* Enables Layout selection ([`0148227`](https://github.com/N5GEH/n5geh.tools.entirety/commit/01482276dd4ec52777ef5398170233c0aa9aecf3))

* fixed: cursor stays default when hovering over text in dropdown ([`db41451`](https://github.com/N5GEH/n5geh.tools.entirety/commit/db41451fcc20104a9ff4b4334d748ecfe12b24f8))

* legend: stack order fixed ([`6f5b602`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6f5b602890d2f79979877e0559f9a30e20533a67))

* Edge coloring ([`8a84e5a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8a84e5a860c61a5b99d25934c68b76bf299961fb))

* parents and children highlighting ([`ea44510`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ea4451014336b70fcdb1769ef5e7f508d06ed672))

* Bug fix: new docker volumes created with every restart (Windows)

Before pulling: docker-compose down
After pulling: superuser &amp; project must be recreated (with old data) ([`4ac732d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4ac732dd7eb9b16616f7e98616263d429f4b1af7))

* Bug fix: node coloring

Nodes return to default color when checkbox is unchecked ([`5ba48e0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5ba48e0873c722094e91749f4c29707d8a4d6ccf))

* Selection of different labels ([`698e1d3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/698e1d37ca147eed144bbe27963bb71d9e9db45f))

* Merge remote-tracking branch &#39;origin/104-integrate-semantics-app&#39; into 104-integrate-semantics-app ([`5cbda24`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5cbda24a16b4d5914856015782b5c79d9394bd84))

* Nodes coloring, legend adjustment

edge coloring will follow ([`fb077df`](https://github.com/N5GEH/n5geh.tools.entirety/commit/fb077df8fb3ece841023830e1c909d13a26b722a))

* Nodes coloring, legend adjustment

relationship coloring will follow ([`6e1d79b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6e1d79b039358f3c94cc01f563b8f3f088045ed0))

* Bugfix: fix deatail-level ([`c6ebb8e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c6ebb8e96d5c823c6601e16c96e4d7066b8fc4d1))

* Adding of several features

-&gt; finishing and styling of entity Table
-&gt; Add Dropdown menu for Legend in main graph
-&gt;Start working on Search feature ([`9806055`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9806055cd7e7d912bb4ed3bea97706e18e4ff77c))

* Integration of entity Tabel

-integration of he entity tabel. No Styling, still default layout ([`6f89454`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6f894547e95fffbfbf24d5b3bdfc6706256e506f))

* Show entity ([`8857f55`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8857f55f9bf9aa7a922bbb528cc4cc9d1a036faf))

* graph zoom limitation ([`692ad4b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/692ad4bcd78c6d29bb90d41111cd5895f6fad810))

* Finished communication with Fiware and added comments

Now the entities will be queried from the context broker and then loaded into the visualisation ([`30f8f84`](https://github.com/N5GEH/n5geh.tools.entirety/commit/30f8f84742292a67d2fba3fce44d4ca3f5426a25))

* Start working on Fiware communication ([`b65fd5c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b65fd5cba0383c5bc685cea3118f1a5c6db89d80))

* update configurations (.env docker-compose) ([`296c026`](https://github.com/N5GEH/n5geh.tools.entirety/commit/296c026b4914c15a5d056748270c4b5b1f98bfab))

* merge dev to 104 ([`267006e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/267006e8cef77938b015e91f663937d75d87f378))

* add sementics views ([`bb24beb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/bb24bebb36687d2a39eccf67b6bcccdf3adc6045))

* Add detail-level ([`0cde5d2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0cde5d2124e92a440163e4e25847f4c117308114))

* safety ([`21c041f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/21c041f821f1c68baa6cb8a250aa21b8c76a2eb9))

* Layout semantics app ([`7b84cce`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7b84ccebe61effc70ea22a3935e86e95e2191139))

* Merge pull request #113 from N5GEH/112-seperate-env-for-db-password-and-user-in-django

112 seperate env for db password and user in django ([`0ddfe1c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0ddfe1ca91f6e0b71d01345504844b13f01efe89))

* 107 include new user flags for user roles (#111)

* chore: include maintainer flag for projects

* chore: update option for maintainer on sidebar

* chore: include widget

* chore: include maintainers in project context

* fix: fixed maintainer function ([`1313e26`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1313e262e0ec3aa291c6274cd8885809b33e4ad0))

* Merge pull request #93 from N5GEH/89-implement-application-level-logging

89 implement application level logging ([`aaf23cd`](https://github.com/N5GEH/n5geh.tools.entirety/commit/aaf23cdaf563e68b6ec76ebf8cb77c9cf8ef6cca))

* Merge pull request #79 from N5GEH/78-implement-service-group

Implement service group ([`29d6c50`](https://github.com/N5GEH/n5geh.tools.entirety/commit/29d6c50919fce33d9913cff453b8506c39dfe02f))

* Merge branch &#39;development&#39; into 78-implement-service-group

# Conflicts:
#	app/Entirety/entities/views.py ([`d9c39c6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d9c39c6764cd0d7f15550c4d8fdafcab710ce12e))

* Merge remote-tracking branch &#39;origin/78-implement-service-group&#39; into 78-implement-service-group

# Conflicts:
#	app/Entirety/devices/utils.py ([`2270636`](https://github.com/N5GEH/n5geh.tools.entirety/commit/2270636f4ab7b7aba8834a2d79c0aa60e6b926d5))

* 95 update contribution guidelines (#96)

* docs: GitHub workflow for development

* docs(fix): docker image

* fix: addition according to review ([`0b94bfe`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0b94bfeb4f17934b4eea171ae7b36e01b2d2e121))

* 90 batch crud entities (#94)

* chore: batch create entity from json

* fix: used filip update function instead of post

* chore: delete batch entities

* chore: force delete entities

* chore: include json icon

* chore: include example in form

* chore: exception handling in list view ([`2a57184`](https://github.com/N5GEH/n5geh.tools.entirety/commit/2a57184a7b4471d38c4e19a910dfed42bb7305ab))

* Merge pull request #92 from N5GEH/91-bugs-in-entities-app

91 bugs in entities app ([`28f2564`](https://github.com/N5GEH/n5geh.tools.entirety/commit/28f2564843866d5e99d839230728ed27e412c9a0))

* add users to project (#63)

* Create PR for #62

* fix: static root for collection

* chore: added users to project option

* chore: enable owner change for server admin

* fix: manual created superuser dose not have superuser access

* fix: project admin should not see all projects

* fix: owner field optional for non-server admins

* fix: project admin limited update options

Co-authored-by: sbanoeon &lt;sbanoeon@users.noreply.github.com&gt;
Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt;
Co-authored-by: JunsongDu &lt;junsong.du@eonerc.rwth-aachen.de&gt;
Co-authored-by: Saira Bano &lt;79838286+sbanoeon@users.noreply.github.com&gt; ([`04f2ef5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/04f2ef5aeb7c0fb8f3b253ae054f7c2263c01f2e))

* WEB_URL missing in settings doc (#83)

* Create PR for #82

* docs(fix): web_url to web_host

Co-authored-by: sbanoeon &lt;sbanoeon@users.noreply.github.com&gt;
Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt; ([`ec03ec3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ec03ec33a24818903a6d34580e8bc4b31bce9679))

* Create PR for #78 ([`7aa980f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7aa980fb6e012d125b5e3cb77db233f71cd07441))

* Merge pull request #75 from N5GEH/74-prevent-oidc-from-storing-password-hashes

prevent oidc from storing password hashes ([`a8938f6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a8938f6a91b12c29b1b6a2cca8a105f3c474c930))

* Create PR for #74 ([`90cbd06`](https://github.com/N5GEH/n5geh.tools.entirety/commit/90cbd06eeef4c0af94cb4b89273237969c63fdc5))

* Merge pull request #69 from N5GEH/68-add-deployment-guide

add deployment guide ([`e43a55d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e43a55d345a72121f2d93b686e63fba8782892db))

* Create PR for #68 ([`a8b5710`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a8b57104cc09ceadd894f1e9d168560d00f62815))

* Merge pull request #67 from N5GEH/main

followup main ([`d50f537`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d50f5371d6f8a599dfd4989065c6b44d8b8ca714))


## v0.4.0 (2022-10-11)

### Chore

* chore: Merge pull request #65 from N5GEH/64-cleanup-environment

cleanup environment ([`75796be`](https://github.com/N5GEH/n5geh.tools.entirety/commit/75796bef93a35e097cf5cfade78420793920d24c))

* chore: cleanup requirements and settings ([`237f6af`](https://github.com/N5GEH/n5geh.tools.entirety/commit/237f6afcca2253c412c582da3a70179dad2149e1))

* chore: add tooltips for notifications ([`2038266`](https://github.com/N5GEH/n5geh.tools.entirety/commit/20382664234e9bcb24fd52042892255d5f7f51df))

* chore: update ([`33e6fd1`](https://github.com/N5GEH/n5geh.tools.entirety/commit/33e6fd13fd4af530a4c068053e06dfd9f5f47347))

* chore: grant server admin full access to all projects ([`a3d3682`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a3d36822326330a8d746997802c8d8953f6fad13))

* chore: suggested change for homepage ([`cb5f652`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cb5f65249ad1796fc02e96f2969ce51978f423e2))

* chore: test dirs ([`0b58946`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0b58946532f42de29ad871a62d823ce1f75c8e2d))

* chore: minor change ([`0f1acc5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0f1acc58737ce05ff8f8ca90198e76438e007a6a))

* chore: updated tooltips ([`a9862c0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a9862c03a50cd718332bf8c6e17627a869648025))

* chore: fix project image size ([`b5a7540`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b5a75407c3cefb8df5b0cb09c8a0a0abd06a8fff))

* chore: Merge pull request #53 from N5GEH/52-fix-subscriptions-app

fix subscriptions app ([`9e50c53`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9e50c538d5a7d118b96a93568bafe04d6fdf9eb1))

### Documentation

* docs: fixed text ([`0eb716a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0eb716a543d4fdc6eab448dd5c969a176bdcfbc7))

* docs: name fix ([`7bc621d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7bc621dea2439d2eef5de7ecf3d0e2bde8dcfb56))

* docs: added subscription tooltip ([`b2ae90b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b2ae90b3f5efeb840b9bef140858712ee377c678))

* docs: fixed class h1 ([`d881ed2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d881ed2353a5ca8bb96b97002665755231ee07be))

* docs: update home page text ([`e8edda8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e8edda8b56b774c07503978c21757fc677aba137))

* docs: include missing settings ([`c500e12`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c500e12109a6e64e5c569bdc709ad7bb64410114))

### Feature

* feat: configurable auth backend (#46)

* Create PR for #45

* feat: login with local user

* fix: fixed admin auth

* chore: url fix

* fix: use admin for user creation

* chore: update requirements

Co-authored-by: dnikolay-ebc &lt;dnikolay-ebc@users.noreply.github.com&gt;
Co-authored-by: dnikolay-ebc &lt;daniel.nikolay@rwth-aachen.de&gt; ([`44335e2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/44335e2eb5d455c586b1f06de65aec034efebcca))

* feat: implement subscriptions app (#49)


Co-authored-by: dnikolay-ebc &lt;dnikolay-ebc@users.noreply.github.com&gt; ([`55e5bf8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/55e5bf8a98ba5a63f54573ff48d0f7cb6e034bde))

### Fix

* fix: added title ([`e004f3d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e004f3d04f14d1099d86c0f450da80de5b2fe959))

* fix: correction ([`ff26e1c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ff26e1ccf6fac58067fbeed616a5b250e377e4c7))

* fix: add missing title for devices ([`40e9098`](https://github.com/N5GEH/n5geh.tools.entirety/commit/40e909896581d0f9e249237c4256a33d0e81b188))

* fix: typo ([`feefe2f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/feefe2f0b2accc53903c28abab0be491ecb1d489))

* fix: typo and type hint ([`d719086`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d719086df7c1b49ab9c32113e0f4b26acc8088d4))

* fix: status above back button ([`4e8c7e0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4e8c7e0f46fa0f5b436286e2cd8eae2a98fd5b9d))

* fix: app selection class change ([`0013abc`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0013abcb9075e6ab6a57131b277222b4e816a891))

* fix: fix empty metadata field ([`b237d68`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b237d683782b0e42b99f955749e76afd0a7f6de7))

* fix: remove page header ([`30d8e82`](https://github.com/N5GEH/n5geh.tools.entirety/commit/30d8e8290239520e8a685bf500834964c9fdb070))

### Unknown

* Merge pull request #66 from N5GEH/development

Create new release ([`37079b7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/37079b7f4ca6edc2ad2585fed6eca84f9d90ce7a))

* Merge pull request #44 from N5GEH/43-roadmap

Roadmap finished before going public. ([`6ae590b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6ae590b4f4c609e6860b7047508a5242674503a3))

* Create PR for #64 ([`5d7b724`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5d7b7242281023f4a9256ba5eec7b5584d59b5da))

* Merge pull request #59 from N5GEH/58-improve-documentation

improve documentation ([`2092bc8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/2092bc88f60216307b8375d12718437073f7b22e))

* Merge remote-tracking branch &#39;origin/58-improve-documentation&#39; into 58-improve-documentation ([`508f482`](https://github.com/N5GEH/n5geh.tools.entirety/commit/508f482a9e84cc6840bae0584cab7b9ca9a761dc))

* Merge pull request #39 from N5GEH/37-validate-attribute-value-in-entities-app

validate attribute value in entities app ([`b6f6ac2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b6f6ac211c4f00881ee3e1faeb164d34b0bb212f))

* Merge pull request #51 from N5GEH/50-image-resize-on-project-overview

Image resize on project overview ([`0506d10`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0506d10024b1f7c34f743dca696f1742bcbbd6f2))

* Merge remote-tracking branch &#39;origin/58-improve-documentation&#39; into 58-improve-documentation ([`bba3655`](https://github.com/N5GEH/n5geh.tools.entirety/commit/bba36556047220dfe600807aea55c59814aa2f36))

* Merge pull request #57 from N5GEH/56-shift-health-status-at-bottom

shift health status at bottom ([`b394b6d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b394b6ddaf206f5022d31ad280b914e42933ef6d))

* Merge branch &#39;58-improve-documentation&#39; of https://github.com/N5GEH/n5geh.tools.entirety2 into 58-improve-documentation ([`66e1d0d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/66e1d0d6c15afa9516ede2ebf05f00b36d28c125))

* Merge branch &#39;50-image-resize-on-project-overview&#39; of https://github.com/N5GEH/n5geh.tools.entirety2 into 50-image-resize-on-project-overview ([`992ecdf`](https://github.com/N5GEH/n5geh.tools.entirety/commit/992ecdfe5326befc8738c375f4d55fec55c0e5c7))

* Merge remote-tracking branch &#39;origin/58-improve-documentation&#39; into 58-improve-documentation ([`0bca867`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0bca8674c4be4afce51a9208b0ba11001af4f2ac))

* Create PR for #58 ([`6547c29`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6547c29839addac7219c5f4ede4ad49bc1fe41a4))

* Create PR for #50 ([`b04e5ae`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b04e5aedcbc541100693d115325ca9f550c4aca2))

* Create PR for #56 ([`5a9c353`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5a9c35303985c818e07366ef80548de6ea728982))

* Merge pull request #55 from N5GEH/54-show-which-app-is-selected

Show which app is selected ([`25139fe`](https://github.com/N5GEH/n5geh.tools.entirety/commit/25139fed5632c621c673a4e89b43b6b2170ebbde))

* Create PR for #54 ([`0f9c108`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0f9c108fd38daf500616759560e3bd7403f8a857))

* Create PR for #52 ([`31493ae`](https://github.com/N5GEH/n5geh.tools.entirety/commit/31493ae6892ef5132e461994dc391f03d8e02109))

* Merge pull request #48 from N5GEH/47-typeerror-type-object-is-not-subscriptable

TypeError: &#39;type&#39; object is not subscriptable ([`119683b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/119683b377568a4afb345ac38865016140bf8435))

* Create PR for #50 ([`e50f51e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e50f51ea627a16cebac5f58a4a430807dac94172))


## v0.3.2 (2022-10-10)

### Chore

* chore: error from filip for attribute ([`e008b8c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e008b8c1ff2e906350b2a6a9b24a3a44cc470509))

* chore: adjust the look of sidebar ([`38b4fb2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/38b4fb24cd4c58c4bdad2d4a31f7e418b8933dea))

* chore: adjust and add tooltips for devices ([`e233edc`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e233edc7f8c34af3870a058a31ea7d97df5bbdac))

* chore: entities app roadmap ([`29e5e85`](https://github.com/N5GEH/n5geh.tools.entirety/commit/29e5e85305dfcc94b7c84c4fff917cc70fb32cba))

* chore: change description of batch create devices ([`97a640c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/97a640c7b9e41497bfb0d9caf812a2dda6a8d0a6))

* chore: add roadmap for devices app ([`5c8e0f2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5c8e0f28d0c172b90e0fc5b1476dc64f553012eb))

* chore: change to 1 second ([`d0b4050`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d0b4050dea615589d12b359a7040fce9b71e8ef8))

* chore: health status on sidebar ([`aef9ea7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/aef9ea7b5d5bec9bcd2bff740d7d411811039d64))

* chore: minor adjustment ([`e44b959`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e44b9599aacd40e05b21228cac1d017e95203ac5))

* chore: create roadmap ([`f09aa29`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f09aa29587c904feebd5c1c3561b723b857bfa49))

* chore: updated entity tooltips ([`284030d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/284030d39f678b16cd5351e337b641d5335c5faa))

* chore: minor change for tooltips ([`418c88a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/418c88afdfe74814a0c0863a1809777d3dfe0a6f))

* chore: application load from env ([`260f700`](https://github.com/N5GEH/n5geh.tools.entirety/commit/260f7006b392737fa234d9576647085aeb02a0db))

* chore: minor change ([`a4f01a1`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a4f01a104f3d97083f91a442e077155c783f6946))

* chore: forward advanced deletion ([`3ace773`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3ace7736ffc018e05911224fc860999071b7d2f1))

* chore: catch validation error ([`0eaac4f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0eaac4f33fb19a8c5b5f5f27c9136d9f7bfbf122))

* chore: non-selection handling ([`7663907`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7663907c9bd0283e0b48383533310c8fcd43e6a6))

* chore: using service and service path from project ([`4c4c00c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4c4c00c36cd66144d53da5b2ab34039fd194448a))

* chore: add advanced deletion modal ([`d1964f5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d1964f54c0e308cae7646e83a02542a62718afbd))

* chore: allow deleting related entity ([`f5c3871`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f5c38710b483626cbb610beba733f4d0deb619da))

* chore: change extra form to 0 ([`86dbb23`](https://github.com/N5GEH/n5geh.tools.entirety/commit/86dbb239ee4b3e21d8a02b38a28af1379a594966))

* chore: show the reason in error message ([`71ae709`](https://github.com/N5GEH/n5geh.tools.entirety/commit/71ae709ff3c6b89219ae473e2a716f71fa658e7d))

* chore: minor change of the table ([`4de6e76`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4de6e76e131d2e2c4a71e3dd160985b4cc70bac7))

* chore: loki settings from env ([`a1e9120`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a1e91201d0b49d7c7b2335c4038b7eb967b3ff0a))

* chore: minor change ([`d38d8c8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d38d8c86d303d6d98ddef9580313501bd1092e03))

* chore: use project context mixin ([`193f25d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/193f25d5b11320b055461d246395a6540f9d2399))

* chore: add close button to message box ([`c5e43e2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c5e43e2fc178fdfe616d461274270cc3b94d210d))

* chore: replace unused class based views with template view ([`c6d794d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c6d794dea5d124c753d9aaa38ee377b2c30012df))

* chore: unify the list view ([`cc24dfe`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cc24dfe7ea271576292b70236d3da5895635fbe4))

* chore: disable editing basic info ([`a55cbd0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a55cbd0c926008c51f4c6b448a419b3fd3f4b91a))

* chore: error handling ([`e5a2107`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e5a21072507c1bdd826c697810ee159e31444310))

* chore: miner change ([`d760653`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d7606536064dac44d1893f073905a6809343c509))

* chore: add error message for devices app ([`9c5db87`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9c5db879e1a119132b936d6276d33c12798c0cf1))

* chore: clean up ([`af653fa`](https://github.com/N5GEH/n5geh.tools.entirety/commit/af653fabeace2d1db3e4a975cf8257d90832e183))

* chore: conditional label on update or create ([`1c67406`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1c67406c685b059d07d5c9b4cba2587ac96654bc))

* chore: filter entity ([`af7e006`](https://github.com/N5GEH/n5geh.tools.entirety/commit/af7e006c0def7d8c6eddd13c6da3ff89c3ce3d6c))

* chore: include attributes in table ([`26b3ee4`](https://github.com/N5GEH/n5geh.tools.entirety/commit/26b3ee4fec8bbf9bc4fae4d4467c3f6106f70091))

* chore: change table view ([`999b4f4`](https://github.com/N5GEH/n5geh.tools.entirety/commit/999b4f4606e372db7706a285666a991b43ecc7ed))

* chore: set checkbox column name and type radio ([`f201931`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f2019317b81b176ecbfdc1a2233a9ed5bdaa9e9d))

* chore: disable fields on update ([`38e42ac`](https://github.com/N5GEH/n5geh.tools.entirety/commit/38e42ac1eef04e423f226aafa38b63b94bc78e9c))

* chore: view for entity crud ([`880e4d6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/880e4d68e7cd7857d5cbe8cc8360c2089b7ec0bd))

* chore: external filip requests ([`ef4f296`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ef4f296f7c049dde0fbbfe0f659db232b55ef4a9))

* chore: delete and update templates ([`4780fc6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4780fc621d72213e28de4274b2f20d7401ef39e6))

* chore: delete entity url inclusion ([`e194cf7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e194cf733a7cbd125c38f3884834c18e2b6dbc7a))

* chore: entity table ([`64995b5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/64995b50257e46218f0ce4e7f19c6753560b8b73))

* chore: include url settings for fiware ([`5051013`](https://github.com/N5GEH/n5geh.tools.entirety/commit/505101351fd2dd6f8c4b4ba58bb41482a365ae58))

* chore: deletion forms ([`c5a32ea`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c5a32eae9013b2505b207309946d3e67cb32ba5c))

* chore: delete and edit buttons with modal ([`d4e6308`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d4e6308f8ba1f3573b4aea766153df8233ac9cd4))

* chore: include conditional addition of accordion ([`81c357d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/81c357df953364a9b69895ffa5f62842ac5e02db))

* chore: add example for message ([`b36f26d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b36f26d97fc58dc358be5484589abbdb23526ae9))

* chore: add message to base template ([`9fbe60d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9fbe60d1c27633df6ea5b943ab7dc67b81534b72))

* chore: add tooltip for basic information ([`23747df`](https://github.com/N5GEH/n5geh.tools.entirety/commit/23747df9d0604cbc8e7f4f07df2d615a4e3396ee))

* chore: change path of devices app ([`37b1f6c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/37b1f6c5d0b170c543a6cc3878fd3e7a343eaec2))

* chore: tooltip for project form ([`093908e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/093908ef35369ce04c84ec6dc69b4de5bc1b605a))

* chore: entity table with django_table2 ([`09f0072`](https://github.com/N5GEH/n5geh.tools.entirety/commit/09f0072009cbdd372b8ef7a83ea413a5ad61a648))

* chore: enable delete devices ([`1730909`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1730909df8ebab35077ae381f414122f9f08081e))

* chore: mini change ([`b117910`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b11791008f54ce38018d98a5cd8e30dcf42ca70f))

* chore: build command list ([`cd7b1e3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cd7b1e3e579f6c91399c4c832381364ae925cb31))

* chore: use dropdown for type, change object_id to optional ([`d262fcf`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d262fcfdac828a7c5a27a6ccae09e855160476e0))

* chore: explicit import functions ([`5f3bf5a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5f3bf5a59f3b01e61b30ccc0c90b23e0930a3499))

* chore: adapt the devices form to accordion ([`ef730d8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ef730d804c993d2843354cd7eb357c79d9258575))

* chore: reference to entities list view ([`e9120d4`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e9120d4d162d819afce30ce1413b48fc9c784c25))

* chore: refactor template ([`5660815`](https://github.com/N5GEH/n5geh.tools.entirety/commit/56608156c64fc1689a5a8044a3a42b41631a95d4))

* chore: project image clickable for detail view ([`b804586`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b8045868fc56170d4ff14e5b332eca6c97816119))

* chore: adding/removing based on class ([`936c584`](https://github.com/N5GEH/n5geh.tools.entirety/commit/936c584fffb22686cd0fb4898f791afb857808ab))

* chore: entities base app ([`53ae8f8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/53ae8f8d9610ed1f397e31c52750ef1a0848ed6c))

* chore: check AAA in devices App ([`5ffd3a6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5ffd3a6d74e48927e0d9477ea4271cbcdbfaebb0))

* chore: add devices app to sidebar ([`ebe9cbe`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ebe9cbe8fcd2b442eda3dd2acb861eb335dc79bc))

* chore: get project data to devices app ([`ab0e26d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ab0e26def7b3694494fdd8bf6e7c2e132716c9ef))

* chore: remove button with js ([`888675f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/888675fca019140e2297e0f9473c0e76887efaef))

* chore: include accordion js for add button ([`1b882f3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1b882f37b7e26bbe88dfeaf917fb8c6800eb802e))

* chore: basic accordion template with formset ([`ed2bbe5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ed2bbe5c47863b8d5621afd74f482ea602ed0242))

### Documentation

* docs: updated notifications roadmap ([`9f05668`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9f05668ae9860dc0c026bf08efe8db0166d6685b))

### Feature

* feat: implement filter for devices ([`6ecefb1`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6ecefb1da3410bf6ad9f8e01a6fd52b0a5a55c42))

* feat: create docker deployment setup

* Create PR for #27

* chore: base docker compose with db

* chore: minor change

* chore: create Dockerfile

* chore: change docker-compose file

* feat: use nginx as web server

* fix: fix media conf

* fix: use template for nginx config

* chore: update env example

* chore: setup docker action

* chore: test workflow

* chore: test docker metadata

* chore: test docker build

* chore: test docker push

* fix: make entrypoint executable

* fix: update compose

* fix: update action

* chore: add release creation to action

* chore: use specific versions in compose

Co-authored-by: sbanoeon &lt;sbanoeon@users.noreply.github.com&gt;
Co-authored-by: Saira Bano &lt;saira.bano@eonerc.rwth-aachen.de&gt;
Co-authored-by: JunsongDu &lt;junsong.du@eonerc.rwth-aachen.de&gt;
Co-authored-by: dnikolay-ebc &lt;daniel.nikolay@rwth-aachen.de&gt; ([`8eb29da`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8eb29da8dfe36e9b6089ec32ffb62db9cbe1ad81))

* feat: implement update device ([`f7b1c7c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f7b1c7c59d3ffd1c3e9986445df2bec8a0f4e052))

* feat: implement device creation ([`73c0efd`](https://github.com/N5GEH/n5geh.tools.entirety/commit/73c0efdf7fe8e09d3c5a24bccc45edf5ccfbe669))

* feat: add first views for devices app ([`3fef918`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3fef918e32e11d7f62bf3563521bfdb2460d37eb))

* feat: implement update device ([`0380489`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0380489e75ab120a9285848f46b7a65350ee2afa))

* feat: implement device creation ([`08fc472`](https://github.com/N5GEH/n5geh.tools.entirety/commit/08fc47233c8e970362bd9eec21e24f0a46922d78))

* feat: add first views for devices app ([`ec8371a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ec8371a8ea480ca5f787a447a1aaaceb16b08c10))

* feat: add first views for devices app ([`7aa5c87`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7aa5c871fd604a0a91dfe32bc5096243f2c86965))

### Fix

* fix: list type hint ([`96d672d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/96d672d5c12b9d07ca25cd2f4027128b4bd51554))

* fix: change interval to 10 secs ([`3aeb92b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3aeb92b299460f748e4fc9d0cd07cd93b428009c))

* fix: add missing mixing for devices ([`22d37c2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/22d37c295c92a8b34ff9635a562a87b2c736f3a1))

* fix: fixed rendering ([`4fba7cb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4fba7cb962cdc26a774f7cbc3d3c50a5d2becdd9))

* fix: fixed attribute tooltip ([`897fe51`](https://github.com/N5GEH/n5geh.tools.entirety/commit/897fe51abcc823d7bb3d63f04e2fa430ccb16627))

* fix: include project fields ([`e12853b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e12853bd023fadc4254af1b9b5c311b46fe41f38))

* fix: minor bug fix ([`ce3c157`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ce3c15770ba45a31dc22fd4d727b42b3277843b4))

* fix: attr type return numbers back ([`ad3cc61`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ad3cc612785a099638d8491934b22aceb8bdeb40))

* fix: included delete entity ([`f6388eb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f6388ebc96ffc11d81fcaf054ce2aac7e2d81528))

* fix: old attribute types ([`2d465ea`](https://github.com/N5GEH/n5geh.tools.entirety/commit/2d465ea148b522dd748280124867633e2f3cb98a))

* fix: included delete devices ([`0f41da4`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0f41da464c6924e1832104bb845a76ee72380c20))

* fix: minor bug fix ([`3b5543a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3b5543a929c00b8c8b69f522fa1624ecd44ee8ed))

* fix: js load bug fix ([`f05d883`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f05d883c8ac5d93151876ec5eb27c8efd3750182))

* fix: fixed bug ([`b548a63`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b548a63c7a90999d3b401c83cc7c3e3430cf09f8))

* fix: include actual request ([`957b19f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/957b19f6b542b58d24cf09d36dab48e1b2dae1c8))

* fix: entity form on error ([`efc3844`](https://github.com/N5GEH/n5geh.tools.entirety/commit/efc3844006fe08708568a047c0a289ce2f110498))

* fix: move script to template ([`3f28348`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3f283482d51a22aedbf5912df6c3ae7a81afd18a))

* fix: wrong total forms number ([`86f6dac`](https://github.com/N5GEH/n5geh.tools.entirety/commit/86f6dac7923a46145424017628854c22a49255dd))

* fix: object_id can be left empty ([`30486be`](https://github.com/N5GEH/n5geh.tools.entirety/commit/30486be57f00c84c2ce1026ec4526defe75211df))

* fix: empty form set in edit mode ([`b0752cd`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b0752cd61af411458539a2ef4169d97f9cd499c9))

* fix: fixed modal title ([`e6b56e9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e6b56e949ef3174aa99cb2bedfcf4dd1b2918ddf))

* fix: loki host name slow the programm down ([`ac66f61`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ac66f61a83f86a45944823c283979f5119352920))

* fix: syntext ([`4010792`](https://github.com/N5GEH/n5geh.tools.entirety/commit/40107924b6fe10baf979b7685251c16bcac287f6))

* fix: re-include loki settings ([`fed076a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/fed076abf5539fe2829a9d629b6d83a1a27db5e7))

* fix: table to include both id and type ([`657da3d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/657da3dfb7ca614523481c81d8bc7d2906aec187))

* fix: maxlength fix and entity type editable ([`d336dcb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d336dcba586a04816c4c64741dee8f78ee1aa87e))

* fix: fixed edit button ([`25f4f9d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/25f4f9dca755d128a1a866342f0571e19769e53b))

* fix: change to filip util subscription function ([`0044ddb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0044ddb11c49f4ff5e33ab36c395959458d7728f))

* fix: correct widget field type ([`e22b8a9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e22b8a90011acf7034e076d3895ea0c5b388c417))

* fix: conditional accordion form render ([`019fdfc`](https://github.com/N5GEH/n5geh.tools.entirety/commit/019fdfc6a0d665a866c40c0e97425da4a6250adb))

* fix: project card alignment with description tooltip ([`de53020`](https://github.com/N5GEH/n5geh.tools.entirety/commit/de53020f4335d89e77c70d844cfb6001b47c69ee))

* fix: remove form tag from internal forms ([`ae7a5d3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ae7a5d3007f318bcbe9f45995afaa0b71dda1f1d))

* fix: use form helper so that all forms are submitted ([`15e8116`](https://github.com/N5GEH/n5geh.tools.entirety/commit/15e81165d0a843bfde43bd4dc1d3b5a03491d997))

* fix: clone empty form instead of first form ([`d6e508c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d6e508c2462583df2786dc4503e74e8797bc4fa4))

* fix: align example ([`0bb8bbb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0bb8bbbe2366f27e3147d2ba284f8056eb7878a2))

* fix: remove checkboxes for remove ([`98c9bf2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/98c9bf28c179781be85f2c423d9ba9c0ed05cac4))

* fix: js console error ([`93f9315`](https://github.com/N5GEH/n5geh.tools.entirety/commit/93f9315f68cadb507e3255beeee31a1bd5ae966b))

### Unknown

* Create PR for #47 ([`4f1a3ef`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4f1a3ef99dbc4f2e7f376981b393f8297ebe0530))

* Update ROADMAP.md

add link ([`74fa959`](https://github.com/N5GEH/n5geh.tools.entirety/commit/74fa959a58f8f832927160968ab1d6bf54bd848a))

* Merge pull request #41 from N5GEH/40-update-tooltip-messages

update tooltip messages ([`1ef4850`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1ef4850cf64ca9fa938c6e7f00be3c7836bdb43b))

* Merge pull request #42 from N5GEH/36-health-status-on-project

health status on project ([`85c7117`](https://github.com/N5GEH/n5geh.tools.entirety/commit/85c7117fa930242d42c068f8b0845135c80298e9))

* Merge branch &#39;development&#39; into 36-health-status-on-project ([`bae54aa`](https://github.com/N5GEH/n5geh.tools.entirety/commit/bae54aae4bae84d3327d1f15b9f3f0ae225921be))

* Merge branch &#39;development&#39; into 40-update-tooltip-messages ([`3c7d522`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3c7d522cdae947c7aab06f248fe429ce3db4436b))

* Merge remote-tracking branch &#39;origin/43-roadmap&#39; into 43-roadmap ([`da1f963`](https://github.com/N5GEH/n5geh.tools.entirety/commit/da1f963a67b4a74f2be2cfdc705dc94dbb04db22))

* Create PR for #43 ([`30939c1`](https://github.com/N5GEH/n5geh.tools.entirety/commit/30939c1cad136cab818b416878fa3e787309df02))

* Merge pull request #16 from N5GEH/15-work-on-devices-app

work on devices app ([`3a0a907`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3a0a9074450ea0a4b818f2c10df3908cee078f59))

* Merge branch &#39;development&#39; into 15-work-on-devices-app ([`329178f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/329178fc7ec406f5c677c4a79bdf319dd2fdae64))

* Create PR for #36 ([`b3503f1`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b3503f19fdc4c889bb58574db7e25a5de6f129a9))

* Create PR for #40 ([`b748f04`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b748f048301563953f7d9988b894858e8eefaeaa))

* Create PR for #37 ([`6b7f8b5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6b7f8b59dfd4af410802662a28b56f24a102d502))

* Merge pull request #38 from N5GEH/35-on-off-application-based-on-env

on-off application based on env ([`35ef6b6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/35ef6b62338b496901ac11b3e8b4517009488214))

* Merge branch &#39;development&#39; into 15-work-on-devices-app ([`eee4281`](https://github.com/N5GEH/n5geh.tools.entirety/commit/eee4281bdfa0818fd92660db35ee941f19566cd0))

* Create PR for #35 ([`d6281ab`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d6281abd29a6c4e8e8d0cb1b8c632a5c7f439cf7))

* Merge pull request #25 from N5GEH/24-work-on-entities-app

work on entities app ([`a7cbcd7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a7cbcd7780dbe91ac7ba3d4c95eee79440673875))

* Merge branch &#39;development&#39; into 24-work-on-entities-app ([`b7dc3ec`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b7dc3ec6fca25aeca892d057e70dc61c55552c58))

* Merge branch &#39;24-work-on-entities-app&#39; into 15-work-on-devices-app ([`8c0ef77`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8c0ef775e81fdafd8ffa189eec2d499c59146cbc))

* Merge branch &#39;development&#39; into 15-work-on-devices-app ([`23b96e8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/23b96e880c1287372f9c8bf0cc57309275950982))

* Merge branch &#39;24-work-on-entities-app&#39; into 15-work-on-devices-app ([`a3b5994`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a3b5994287ac4dc514738642b1be4468ea9bf943))

* Merge pull request #34 from N5GEH/33-dictionary-type-settings-in-pydantic

Dictionary type settings in pydantic ([`a970a36`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a970a362c7450f70580751860a7f95f0ff4d0988))

* Merge branch &#39;24-work-on-entities-app&#39; into 15-work-on-devices-app ([`5c0f4c4`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5c0f4c4edf71011fe0445e6425f6e693c6bd97d9))

* Create PR for #33 ([`cf2ec3e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cf2ec3e645ab81dd42c4919d661238ac9428be16))

* Merge branch &#39;24-work-on-entities-app&#39; into 15-work-on-devices-app ([`6ab042a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6ab042a871940ca5a49b0cae0b5ae06465df5663))

* Merge branch &#39;development&#39; into 15-work-on-devices-app ([`73b0c1d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/73b0c1d4ae547aac646e821ef546de5c384984a0))

* Merge pull request #32 from N5GEH/31-fix-logging-in-settings

Fix logging in settings ([`cbd0845`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cbd08451720710803256ed0fef9ab5bcc346cc1b))

* Create PR for #31 ([`1145eeb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1145eeba5f5c8ee508145a2812d6a35a05827b69))

* Merge branch &#39;24-work-on-entities-app&#39; into 15-work-on-devices-app ([`96e4c13`](https://github.com/N5GEH/n5geh.tools.entirety/commit/96e4c13bfc86f82252f008f1ffb2b768da09041c))

* Merge pull request #30 from N5GEH/29-general-way-to-display-error-message

general way to display error/warning/success message ([`ff34cd2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ff34cd2b3fb9ab84a290553ba3da13b9fb230adf))

* Create PR for #29 ([`72cccfd`](https://github.com/N5GEH/n5geh.tools.entirety/commit/72cccfd9bc7c25090f88c02f31c947bd95315c8f))

* Merge branch &#39;21-implement-accordion-template-for-apps&#39; into 15-work-on-devices-app ([`256e171`](https://github.com/N5GEH/n5geh.tools.entirety/commit/256e171b8ee69923f628aec747ddfe3ea664a6d6))

* Merge branch &#39;21-implement-accordion-template-for-apps&#39; into 24-work-on-entities-app ([`43f8f1b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/43f8f1bb5f2c66bd8e3c3390aa232dbdfc34a62e))

* Create PR for #24 ([`35b7743`](https://github.com/N5GEH/n5geh.tools.entirety/commit/35b77437f6c2c2016f9d9e7a2e086cc418d23ba6))

* Merge branch &#39;15-work-on-devices-app&#39; of https://github.com/N5GEH/n5geh.tools.entirety2 into 15-work-on-devices-app ([`eef330d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/eef330d0291df009faa2377047da5b290df09453))

* Create PR for #15 ([`3433f04`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3433f04989c47a6763a832a1cb25e647ba484ecb))

* Create PR for #15 ([`5173353`](https://github.com/N5GEH/n5geh.tools.entirety/commit/51733537d57fb7d03d57f796f5181266d29d3ac1))

* Create PR for #15 ([`5d4c7b8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5d4c7b83845736d28d8617ec1a3fb2d4e5ba0a6b))

* Create PR for #15 ([`32a1122`](https://github.com/N5GEH/n5geh.tools.entirety/commit/32a1122330d450fbd0d33dced798e4708c93d03f))

* Merge branch &#39;15-work-on-devices-app&#39; of https://github.com/N5GEH/n5geh.tools.entirety2 into 15-work-on-devices-app ([`a2e17c7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a2e17c7c12ca209aa4151d3dd4502047b4fa5f55))

* Create PR for #15 ([`6a4d612`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6a4d6126083e8872da320b08236d7e56b9886509))

* Create PR for #15 ([`5a37862`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5a37862e7a0d545feff351212eb7538fddcbe828))

* Merge pull request #10 from N5GEH/9-implement-logging-for-application

implement logging for application ([`6216394`](https://github.com/N5GEH/n5geh.tools.entirety/commit/62163942c4b1aba5e8aec52a91836f27f363d1a7))

* Merge branch &#39;main&#39; into 9-implement-logging-for-application ([`116eadd`](https://github.com/N5GEH/n5geh.tools.entirety/commit/116eadd98b0727c27f73cab5e51b8b9d71b6f881))

* Merge branch &#39;15-work-on-devices-app&#39; of https://github.com/N5GEH/n5geh.tools.entirety2 into 15-work-on-devices-app ([`110dcc6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/110dcc646b10408255013c959c3248f7ae4135b1))

* Create PR for #21 ([`cbaea5d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/cbaea5d0d98a49acc53d3d43d2513426a1e853d4))

* Create PR for #15 ([`2a4336a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/2a4336ad77c2964aef63903ede929f51665ffb86))


## v0.3.1 (2022-07-21)

### Chore

* chore: example logging in view ([`48acb67`](https://github.com/N5GEH/n5geh.tools.entirety/commit/48acb6756c3037a10a2e3e4cebb3b3e93b2290be))

* chore: pass all logs to loki ([`77b3f23`](https://github.com/N5GEH/n5geh.tools.entirety/commit/77b3f23d87476fd3f00fe43dc897630fb2bebcf7))

* chore: template view based on user and list class for projects ([`9166f4e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9166f4ed19a444bb89199ff8422ddd807852ff38))

* chore: project mixins ([`c305e10`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c305e10c658696ec0f6ad7fb8ea39c35c0fdc7f0))

### Fix

* fix: fixed card grid to auto ([`72e2c71`](https://github.com/N5GEH/n5geh.tools.entirety/commit/72e2c714a5a4022ab002d1216e0b32245a7bd602))

* fix: delete unused view structure ([`d1ed9c8`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d1ed9c8822c3670c413b3580ee2e733cd2278ec2))

* fix: project context mixin ([`e1d22c0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e1d22c0774c35357777ec16568305ba55efcf83c))

* fix: re-activated alarming url ([`98c8f43`](https://github.com/N5GEH/n5geh.tools.entirety/commit/98c8f4300c6bb81270fda6134fd0980c97bf20da))

### Unknown

* Merge pull request #18 from N5GEH/17-auth-in-projects-app

auth in projects app ([`4e20613`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4e20613c4485db89a34a97efafc0c1f277a45938))


## v0.3.0 (2022-07-18)

### Chore

* chore: added loki logging ([`3a01b1c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3a01b1c8b6f516b411e6bb05224a63172ecde632))

### Documentation

* docs: update requirements.txt ([`746bc0a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/746bc0acc5d5580b8bf3b065be1c20fc93cf91e1))

### Fix

* fix: remove unused code ([`01d4ca2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/01d4ca2a13ccd230c6be710ff34cb240eb375fb8))

* fix: corrected timezone ([`1b4c1ca`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1b4c1ca6cb218f056b1a247b366fa84717bc7d1a))

### Refactor

* refactor: style using boostrap classes instead of custom style ([`275bd41`](https://github.com/N5GEH/n5geh.tools.entirety/commit/275bd414dd3c23fd35fea6cc3353b4f17475051b))

### Unknown

* Create PR for #17 ([`0f0e6f1`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0f0e6f19ef04b20b0992dd5bf3deb6be4936f403))

* Merge pull request #4 from N5GEH/3-Work-on-projects-application

Work on projects application ([`8749ea0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8749ea0b9f4fd3006ca06ebe44ba91170d4acb59))

* Create PR for #15 ([`fc3c64c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/fc3c64c20fb7e9a25576667d30bd214a40fe1a40))


## v0.2.1 (2022-07-18)

### Chore

* chore: fix typo ([`f0ec3ba`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f0ec3bad5c2db157af6e55aebbbb83acc07838fc))

* chore: exclude js/css frameworks from language detection ([`11e8404`](https://github.com/N5GEH/n5geh.tools.entirety/commit/11e84045048d9ae4285d092446ca2702815a0eba))

* chore: use lowercase branch names ([`1ff5aca`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1ff5acac1ded69eeef6a8b88d2a5475c79003dc8))

* chore: exclude js/css frameworks from language detection ([`dc46507`](https://github.com/N5GEH/n5geh.tools.entirety/commit/dc46507c3240dda03f2c93a8150ff3b964d776bb))

### Fix

* fix: remove extra line ([`31c9e5c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/31c9e5caba5832ce57579600d510bf2e95bc9cc4))

* fix: database setting ([`bb4750c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/bb4750c4ca31164cf216a9b73e68a2ad0745763f))

* fix: use oidc auth in django admin ([`d4d862d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d4d862de39c808cb8b8a4d2a5744aca1679423c6))

* fix: project reference ([`bb8f59e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/bb8f59e5a84eb71d6838437b3c86fc7a9057e61c))

* fix: project card alignment ([`4c93b1c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4c93b1c1fad0a2a70fee4130699c37df85d633a2))

### Refactor

* refactor: restructure examples app ([`19de04e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/19de04effb3689f6dbae2f61f080d62ecfb8f95b))

### Unknown

* Merge pull request #12 from N5GEH/11-redirect-admin-to-oidc-provider

redirect admin to oidc provider ([`49f88e7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/49f88e7002db8bd7dc1f5c5b7896716e1d3fffa0))

* Merge remote-tracking branch &#39;origin/main&#39; into 9-implement-logging-for-application ([`ab45244`](https://github.com/N5GEH/n5geh.tools.entirety/commit/ab452449659100b37db1c3b8ad9d394933870459))

* Merge remote-tracking branch &#39;origin/main&#39; into 3-Work-on-projects-application

# Conflicts:
#	app/Entirety/entirety/settings.py
#	app/Entirety/entirety/urls.py
#	app/Entirety/projects/models.py
#	app/Entirety/projects/templates/projects/index.html
#	app/Entirety/projects/urls.py
#	app/Entirety/projects/views/index.py
#	app/Entirety/requirements.txt
#	app/Entirety/templates/sidebar.html ([`d2d1c0f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/d2d1c0f744949d645f160d29960c34c894df2958))

* Create PR for #11 ([`95d919a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/95d919ae59de021b70583dc5e1561d13eb50909a))

* Merge pull request #8 from N5GEH/7-Hackathon_1

Hackathon_1 ([`3a1f5c0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3a1f5c0520366a8cf0230db7b0386d97701f8439))

* Merge branch &#39;7-Hackathon_1&#39; of https://github.com/N5GEH/n5geh.tools.entirety2 into 7-Hackathon_1 ([`e4ba278`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e4ba2787f8567eb6275742e38a0bd44565152549))

* Create PR for #7 ([`6621a70`](https://github.com/N5GEH/n5geh.tools.entirety/commit/6621a700ba53eb3eb1cb5a2708adead10e2fb60f))


## v0.2.0 (2022-07-15)

### Chore

* chore: delete modal and search bar styling ([`80c738f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/80c738f6706185fa4ae46aa162bf514adcaff039))

* chore: made project name unique ([`8fea285`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8fea285eb8390f413e3620f5eb741890ea076691))

* chore: add alarming app for testing purposes ([`1d166de`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1d166de533ed73f73059d00cc682c266c75a80ee))

* chore: add user model meta info to database ([`df4fcbb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/df4fcbb9cfeeb53854cd7b565c5afc3442219dd2))

* chore: cleanup templates ([`5bd2f78`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5bd2f7820adb2fe70c47bed60e66ccb2381453e4))

* chore: add super_admin to staff ([`2cb2d1d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/2cb2d1d65501734dccf2e16f3b3430fa0e43aa45))

* chore: clean settings ([`80d5e99`](https://github.com/N5GEH/n5geh.tools.entirety/commit/80d5e99dbf718236c32dd267c5f731f261e04435))

* chore: fix language code default ([`0bb28b9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/0bb28b90e8838fb813f7c5d2e2f27e0fb0420a59))

* chore: add oidc provider ([`07c4cdb`](https://github.com/N5GEH/n5geh.tools.entirety/commit/07c4cdb07407807c3860566b33761b05b89aabe0))

### Documentation

* docs: move settings to seperate file ([`09688b9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/09688b909253012788dbabb61bcc247e5818ddb6))

* docs: add changelog and contributing to readme ([`18a2a73`](https://github.com/N5GEH/n5geh.tools.entirety/commit/18a2a73012117707f60120624d516a0e4f3d1aa8))

* docs: contribution guidelines added ([`953f61a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/953f61a6e77f1099a56b66866ac44ca94e1cfbc3))

* docs: update requirements for image upload ([`8940b96`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8940b96c20e53dc72408a46b9900392857e229c1))

* docs: add env variable description to readme ([`557e9a6`](https://github.com/N5GEH/n5geh.tools.entirety/commit/557e9a672f4294fe06b64da0ac0a8e84a81d41e7))

* docs: update requirements ([`3a01011`](https://github.com/N5GEH/n5geh.tools.entirety/commit/3a010116cd25210a3e375c7e02a91ab10f651cf4))

### Feature

* feat: add custom error pages ([`a84053a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a84053a41948fde9dd9178c7d97a1e55c35dd4f5))

* feat: raise a HTTP 403 if user is not authorized ([`a556bdd`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a556bdd89bae486421ed1894e344a6f061db6282))

* feat: run apps in project context ([`fcc4f0a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/fcc4f0a6a8fd3c8e8da7ceb554a6e039969e1e04))

* feat: projects create and update view with form ([`a7fc8f7`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a7fc8f70ea810099baeddda73d1a8b55750de3a8))

* feat: make sidebar sticky ([`8bd132f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8bd132fede464380e7f62ac6a9526e8c03e6ef87))

* feat: get authorization parameters from settings ([`7ca3e49`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7ca3e49e0b75e689d24131c0acd17d1b7cfd8fa9))

* feat: add user profile page ([`4e0f757`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4e0f757a8b748cb88fc9437a56e3e60105866f6d))

* feat: add basic authorization ([`03ab314`](https://github.com/N5GEH/n5geh.tools.entirety/commit/03ab3148e3746a1cefd25ea1d292b6fae0e70db0))

* feat: pydantic settings setup ([`c90c031`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c90c031e5cd85fb1659f6fd984be6259525bd1b9))

* feat: require login for view ([`1151c93`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1151c93ea9074ca17ebb6f695f3c9b5afe594812))

* feat: login/logout implemented ([`c0cd1aa`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c0cd1aa67662b253cd2a33da7ddfd71168a684da))

* feat: use pydantic settings ([`5499f10`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5499f10625cc02d77c36de2126b72df09ad78997))

* feat: add user settings to ui template ([`1ba1c29`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1ba1c29c461090f6f2ba20fbd4510b0520d16bc7))

* feat: projects application model view ([`f2d0060`](https://github.com/N5GEH/n5geh.tools.entirety/commit/f2d0060ce18658f52e8365773a7de841e2c973eb))

### Fix

* fix: show project name after selection ([`a2cd2af`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a2cd2af31c8bab7b704a2e598ecc279ce46074a6))

* fix: remove extra parameter
No need to add form.helper if the FormHelper attribute is named helper (in forms.py) ([`41fa198`](https://github.com/N5GEH/n5geh.tools.entirety/commit/41fa198a6db9152ded33bd684c976d018177d8e9))

* fix: corrected braces ([`aa402f9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/aa402f92fd85a57b8b6d03981c9d1a2ba81be4b7))

* fix: crispy form settings bootstrap5 ([`6782418`](https://github.com/N5GEH/n5geh.tools.entirety/commit/678241889b7e0360a1413dfa50d27b25c658df5c))

* fix: scrollbar styling ([`b278c8a`](https://github.com/N5GEH/n5geh.tools.entirety/commit/b278c8a8ca3bdd7b667aacb139f47323abcc412d))

* fix: set sidebar link active ([`a792b1f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a792b1f6eda3c771ff834c752c9216f4bf8bde96))

* fix: fix requirements and settings ([`1848ca3`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1848ca32b2df9b87515b074fdb8d4f8705f7018c))

### Unknown

* Merge pull request #6 from N5GEH/5-add-oidc-auth

add oidc auth ([`33ed830`](https://github.com/N5GEH/n5geh.tools.entirety/commit/33ed8307ee78146c8ee334870068edd88d276fec))

* Create PR for #9 ([`32e4df0`](https://github.com/N5GEH/n5geh.tools.entirety/commit/32e4df0e6a64f830f84cb7f53403823249cb4a1f))

* Create PR for #7 ([`95cc8b9`](https://github.com/N5GEH/n5geh.tools.entirety/commit/95cc8b98a70136b447dd3d0dc04f88521078ad44))

* Merge branch &#39;main&#39; into 3-Work-on-projects-application

# Conflicts:
#	app/Entirety/entirety/settings.py
#	app/Entirety/entirety/urls.py
#	app/Entirety/projects/templates/projects/index.html ([`c9c2025`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c9c2025519afe439e32dbb435667134dc12fbf71))

* Create PR for #5 ([`144408c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/144408cf091ca9a945437ae961f7faf1995f5c04))


## v0.1.0 (2022-06-29)

### Chore

* chore: fix typo ([`8633ebe`](https://github.com/N5GEH/n5geh.tools.entirety/commit/8633ebebd09fdf156c0889be132b235ae421d4b8))

* chore: Merge pull request #2 from N5GEH/1-create-base-ui

create base ui ([`a2e34cc`](https://github.com/N5GEH/n5geh.tools.entirety/commit/a2e34ccca8f4162d37323d0b099c4594279f17fe))

* chore: updated requirements ([`19b5b9d`](https://github.com/N5GEH/n5geh.tools.entirety/commit/19b5b9db5dd62927fd29f9a119ee07908e157495))

* chore: use crispy forms ([`5179429`](https://github.com/N5GEH/n5geh.tools.entirety/commit/5179429472cd7059f7bf2942f28c2c087a27ff59))

* chore: modal form as template ([`e393977`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e3939773c2fe85570151723a527ef7f8671fb841))

* chore: add semantic release ([`5508397`](https://github.com/N5GEH/n5geh.tools.entirety/commit/550839769783bddd548e7616e65a5ec2bc2d8757))

* chore: example url in sidebar ([`173c7de`](https://github.com/N5GEH/n5geh.tools.entirety/commit/173c7de045d67f3d93d33d6c7f5922cd9e61d0b0))

* chore: use scss ([`c832712`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c8327122fdebd683e7e1e79bcf9419fefd1fcf93))

* chore: add navbar ([`4fa3bc4`](https://github.com/N5GEH/n5geh.tools.entirety/commit/4fa3bc46e7883fb904ca8bc6432dc8c2ab91e6bb))

* chore: use local resources ([`e942c3f`](https://github.com/N5GEH/n5geh.tools.entirety/commit/e942c3f1f1fbf5e9f0957c6bfa854f8d8e16d474))

* chore: base repo setup ([`671f17c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/671f17c1d51cdcdbc699e3136f90edb0d635802c))

### Documentation

* docs: update contact ([`9e52b64`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9e52b64c98a5684fca05bb5ca251229108b65982))

* docs: add install instructions ([`7c0c1f5`](https://github.com/N5GEH/n5geh.tools.entirety/commit/7c0c1f50434059af190b70b80e3643619dd7eefe))

### Feature

* feat: add success message toast ([`30acd77`](https://github.com/N5GEH/n5geh.tools.entirety/commit/30acd77dc0d2e7f6c0744c1fceaf750c21d76d4f))

* feat: dialog template with example ([`02b485b`](https://github.com/N5GEH/n5geh.tools.entirety/commit/02b485b1f28650b03bea0e399d0a2950ff1703c5))

* feat: collapsible sidebar ([`c7fefb2`](https://github.com/N5GEH/n5geh.tools.entirety/commit/c7fefb2c2b67f033db534005d294d7c3a70a015b))

* feat: create base app structure ([`366bf73`](https://github.com/N5GEH/n5geh.tools.entirety/commit/366bf7332a2eddccada6f28aa16af34a7ab3191a))

### Fix

* fix: show sidebar tooltips only on small screen ([`24cb298`](https://github.com/N5GEH/n5geh.tools.entirety/commit/24cb29812284a09426dfea079b72b86cfdd1c4f7))

* fix: fix sidebar adjustment ([`db8081c`](https://github.com/N5GEH/n5geh.tools.entirety/commit/db8081cd504629bca3c7644267837a336e103f53))

* fix: fix admin page css ([`646808e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/646808efbbd603e273ca8351532770d49a61bd16))

### Unknown

* Merge remote-tracking branch &#39;origin/1-create-base-ui&#39; into 3-Work-on-projects-application ([`270c67e`](https://github.com/N5GEH/n5geh.tools.entirety/commit/270c67e27cde667fc6dc3e1b8b590d0c997d46cc))

* Create PR for #3 ([`1cc1cdc`](https://github.com/N5GEH/n5geh.tools.entirety/commit/1cc1cdc9ff916ba6e65db2a17bc192950db3c80e))

* Create PR for #1 ([`dfe3dfe`](https://github.com/N5GEH/n5geh.tools.entirety/commit/dfe3dfe6a9e3685f33bc1d174b61611e7dc0ff35))

* Initial commit ([`9871a06`](https://github.com/N5GEH/n5geh.tools.entirety/commit/9871a06e91e83fb062f45f465484682d33b2bd42))

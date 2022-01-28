## Change Log

### v1.3 (2022/1/27)
- Updated to support Python3

### v1.2 (2021/5/17)
- Added Microsoft Teams

### v1.1 (2020/2/17)
- Fixed the ordering of the message_subject argument for the incident/maintenance methods which was breaking backwards compatibility

### v1.0 (2020/2/14)
- Change silent param for subscriber/add to a string (@incarnate)

### v0.9 (2020/2/10)
- Added message_subject to the maintenance schedule, start, update and finish methods
- Adding message_subject to the incident create, update and resolve (@cfrancocapo)

### v0.8 (2018/11/28)
- Changed variables to proper type (int->str)

### v0.7 (2018/2/10)
- Change /component/status/update to use a single component
- Support retrieving single incident/maintenance events
- New incident/maintenance methods to fetch list of IDs

### v0.6 (2017/12/20)
- Updated for incident/create infrastructure_affected

### v0.5 (2017/12/14)
- Updated for maintenance/schedule infrastructure_affected

### v0.4 (2017/1/26)
- Fixed error messages

### v0.3 (2016/1/7)
- Initial release

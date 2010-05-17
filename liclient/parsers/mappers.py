from lxml import etree
import datetime, re
import lixml
    
class LinkedInData(object):
    def __init__(self, data, xml):
        self.xml = xml
        self.parse_data(data)
    
    def parse_data(self, data):
        for k in data.keys():
            self.__dict__[k] = data[k]
            
    def jsonify(self):
        json = {}
        for k in self.__dict__.keys():
            if type(self.__dict__[k]) == type(''):
                json[k] = self.__dict__[k]
        return json
        
    def xmlify(self):
        converted = [re.sub('_', '-', k) for k in self.__dict__.keys()]
        for d in self.xml.iter(tag=etree.Element):
            if d.tag in converted:
                try:
                    d.text = self.__dict__[re.sub('-', '_', d.tag)]
                except:
                    continue
        return etree.tostring(self.xml)
    
    def __str__(self):
        return self.update_content if self.update_content else '<No content>'
    
class LinkedInError(LinkedInData):
    def __repr__(self):
        return '<LinkedIn Error code %s>'.encode('utf-8') % self.status
        
class NetworkUpdate(LinkedInData):
    def __init__(self, data, xml):
        self.xml = xml
        self.update_key = None
        self.parse_data(data)
        
    def jsonify(self):
        jsondict = {'first_name': self.first_name,
                    'last_name': self.last_name,
                    'update_content': self.update_content,
                    'timestamp': self.timestamp,
                    'update_key': self.update_key,
                    'profile_url': self.profile_url}
        return jsondict
    
class NetworkStatusUpdate(NetworkUpdate):
    def __init__(self, data, xml):
        self.status_xpath = etree.XPath('update-content/person/current-status')
        self.comment_xpath = etree.XPath('update-comments/update-comment')
        self.update_key = None
        self.xml = xml
        self.parse_data(data)
        self.update_content = self.status_xpath(xml)[0].text.strip()
        self.comments = []
        self.get_comments()
        
    def get_comments(self):
        for c in self.comment_xpath(self.xml):
            comment = NetworkUpdateComment(c)
            self.comments.append(comment)
        return

class NetworkConnectionUpdate(NetworkUpdate):
    def __init__(self, data, xml):
        self.xml = xml
        self.update_key = None
        self.parse_data(data)
        self.connection_target = etree.XPath('update-content/person/connections/person')
        self.targets = []
        self.get_targets()
        self.set_update_content(self.targets)
    
    def get_targets(self):
        for p in self.connection_target(self.xml):
            obj = lixml.LinkedInProfileParser(p).results
        self.targets = obj
    
    def set_update_content(self, targets):
        update_str = self.first_name + ' ' + self.last_name + ' is now connected with '
        if len(targets) == 1:
            update_str += targets[0].first_name + ' ' + targets[0].last_name
        else:
            for t in targets:
                update_str += t.first_name + ' ' + t.last_name + ', and '
        update_str = re.sub(', and $', '', update_str)
        self.update_content = update_str
        return

class NetworkNewConnectionUpdate(NetworkConnectionUpdate):
    def get_targets(self):
        self.connection_target = etree.XPath('update-content/person/')
        for p in self.connection_target(self.xml):
            obj = LinkedInProfileParser(p).results
        self.targets = obj
    
    def set_update_content(self, target):
        update_str = ' is now connected with you.'
        update_str = targets[0].first_name + ' ' + targets[0].last_name + update_str
        self.update_content = update_str
        return
    
class NetworkAddressBookUpdate(NetworkNewConnectionUpdate):
    def set_update_content(self, target):
        update_str = ' just joined LinkedIn.'
        update_str = self.targets[0].first_name + ' ' + self.targets[0].last_name + update_str
        self.update_content = update_str
        return

class NetworkGroupUpdate(NetworkUpdate):
    def __init__(self, data, xml):
        self.update_key = None
        self.xml = xml
        self.parse_data(data)
        self.group_target = etree.XPath('update-content/person/member-groups/member-group')
        self.group_name_target = etree.XPath('name')
        self.group_url_target = etree.XPath('site-group-request/url')
        self.targets = []
        self.get_targets()
        self.set_update_content(self.targets)
    
    def get_targets(self):
        for g in self.group_target(self.xml):
            target_dict = {}
            k = self.group_name_target(g)[0].text.strip()
            v = self.group_url_target(g)[0].text.strip()
            target_dict[k] = v
            self.targets.append(target_dict)
        return
    
    def set_update_content(self, targets):
        update_str = self.first_name + ' ' + self.last_name + ' joined '
        if len(targets) == 1:
            update_str += '<a href="'+targets[0].values()[0]+'">'+targets[0].keys()[0] + '</a>'
        else:
            for t in targets:
                update_str += '<a href="'+t.values()[0]+'">'+t.keys()[0] + '</a>, and '
        update_str = re.sub(', and $', '', update_str)
        self.update_content = update_str
        return
    
class NetworkQuestionUpdate(NetworkUpdate):
    def __init__(self, data, xml):
        self.xml = xml
        self.update_key = None
        self.parse_data(data)
        self.question_title_xpath = etree.XPath('update-content/question/title')
        self.set_update_content()
    
    def set_update_content(self):
        update_str = self.first_name + ' ' + self.last_name + ' asked a question: '
        qstn_text = self.question_title_xpath(self.xml)[0].text.strip()
        update_str += qstn_text
        self.update_content = update_str
        return
    
class NetworkAnswerUpdate(NetworkUpdate):
    def __init__(self, data, xml):
        self.update_key = None
        self.xml = xml
        self.parse_data(data)
        self.question_title_xpath = etree.XPath('update-content/question/title')
        self.answer_xpath = etree.XPath('update-content/question/answers/answer')
        self.get_answers()
        self.set_update_content()
    
    def get_answers(self):
        for a in self.answer_xpath(self.xml):
            self.profile_url = a.xpath('web-url')[0].text.strip()
            self.first_name = a.xpath('author/first-name')[0].text.strip()
            self.last_name = a.xpath('author/last-name')[0].text.strip()
    
    def set_update_content(self):
        update_str = self.first_name + ' ' + self.last_name + ' answered: '
        qstn_text = self.question_title_xpath(self.xml)[0].text.strip()
        update_str += qstn_text
        self.update_content = update_str
        return
    
class NetworkJobPostingUpdate(NetworkUpdate):
    def __init__(self, data, xml):
        self.xml = xml
        self.parse_data(data)
        self.set_update_content()
        self.poster = lixml.LinkedInXMLParser(xml.xpath('job-poster')[0])
    
    def set_update_content(self):
        update_str = self.poster.first_name + ' ' + self.poster.last_name + ' posted a job: ' + self.job_title
        self.update_content = update_str
        return

class NetworkUpdateComment(LinkedInData):
    def __init__(self, xml):
        self.xml = xml
        self.comment_xpath = etree.XPath('comment')
        self.person_xpath = etree.XPath('person')
        self.__content = lixml.LinkedInXMLParser(etree.tostring(self.person_xpath(xml)[0])).results[0]
        self.first_name = self.__content.first_name
        self.last_name = self.__content.last_name
        self.profile_url = self.__content.profile_url
        self.update_content = self.comment_xpath(xml)[0].text
        
    def jsonify(self):
        jsondict = {'first_name': self.first_name,
                    'last_name': self.last_name,
                    'update_content': self.update_content,
                    'profile_url': self.profile_url}
        return jsondict

class Profile(LinkedInData):
    def __init__(self, data, xml):
        self.profile_url = ''
        self.xml = xml
        self.parse_data(data)
        self.positions = []
        self.educations = []
        if not self.profile_url:
            self.set_profile_url()
        self.get_positions()
        self.get_educations()
        
    def set_profile_url(self):
        try:
            profile_url_xpath = etree.XPath('site-standard-profile-request/url')
            self.profile_url = profile_url_xpath(self.xml)[0].text.strip()
        except:
            pass
        
    def get_positions(self):
        profile_position_xpath = etree.XPath('positions/position')
        pos = profile_position_xpath(self.xml)
        for p in pos:
            obj = lixml.LinkedInXMLParser(etree.tostring(p)).results
            self.positions.append(obj)
    
    def get_educations(self):
        profile_education_xpath = etree.XPath('educations/education')
        eds = profile_education_xpath(self.xml)
        for e in eds:
            obj = lixml.LinkedInXMLParser(etree.tostring(e)).results
            self.educations.append(obj)
        
class Position(LinkedInData):
    pass

class Education(LinkedInData):
    pass
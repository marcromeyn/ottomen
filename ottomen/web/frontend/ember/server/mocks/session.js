module.exports = function(app) {
  var express = require('express');
  var sessionRouter = express.Router();

  sessionRouter.get('/', function(req, res) {
    res.send({
      'session': []
    });
  });

  sessionRouter.post('/', function(req, res) {
    console.log({params: req.param()})
    res.send({
      'session': {
        id: 'XXXX',
        questions: ["J3Xq5m", "JNFAmM", "Jwhfvg", "K7AQ0b", "LlfA_6"],
        worker_id: 'w123',
        task_id: 'test123',
        questions_type: "boolean"
      },
      'questions': [{
        id: "J3Xq5m",
        text: "For more than two decades, our research teams from Slovakia, Russia, Canada, Netherlands, Latin America and the US worked on hundreds of projects uncovering series of events related to hackers and other cyber criminals activities including less worrying samples to sophisticated and targeted attacks such as ACAD projects stealthy ACAD/Medre, military focused Georgian Georbot, very first impactful mac Flashback Trojan or the Linux/Cdorked.A apache webserver backdoor, analyzing their methodology and tracking their origins as well as the malware spread, helping users, companies and government institutions around the world to stay and feel protected.",
        answers: ["ACAD/Medre"]
      }, {
        id: "JNFAmM",
        text: "Four specific families of threats contributed to the steep rise in the malware infection rates of Austria, Germany, Italy, and the Netherlands: Win32/EyeStye, Win32/Zbot (also known as Zeus), Win32/Keygen, and Blacole.",
        answers: ["Blacole"]
      }, {
        id: "Jwhfvg",
        text: "If the Jokra packer is limited to the one group, then the connections between Backdoor.Prioxer and Trojan.Jokra are reliable.",
        answers: ["Jokra"]
      }, {
        id: "K7AQ0b",
        text: "If the file, detected as TrojanDownloader:Win32/Filcout.A, is loaded in a computer with a vulnerability exploited by Blacole, it may download and run arbitrary files.",
        answers: ["Blacole"]
      }, {
        id: "LlfA_6",
        text: "Instead of redirecting to innocent pages with Google adware or porn affiliate site, it takes you to a site which pushes malware (the malware is Zlob related, and detected by Sophos as Troj/Zlobar-Fam ).",
        answers: ["Zlob"]
      }]
    });
  });

  sessionRouter.get('/:id', function(req, res) {
    res.send({
      'session': {
        id: 'XXXX',
        questions: ["J3Xq5m", "JNFAmM", "Jwhfvg", "K7AQ0b", "LlfA_6"],
        worker_id: 'w123',
        task_id: 'test123',
        questions_type: "boolean"
      },
      'questions': [{
        id: "J3Xq5m",
        text: "For more than two decades, our research teams from Slovakia, Russia, Canada, Netherlands, Latin America and the US worked on hundreds of projects uncovering series of events related to hackers and other cyber criminals activities including less worrying samples to sophisticated and targeted attacks such as ACAD projects stealthy ACAD/Medre, military focused Georgian Georbot, very first impactful mac Flashback Trojan or the Linux/Cdorked.A apache webserver backdoor, analyzing their methodology and tracking their origins as well as the malware spread, helping users, companies and government institutions around the world to stay and feel protected.",
        answers: ["ACAD/Medre", "Linux/Cdorked"]
      }, {
        id: "JNFAmM",
        text: "Four specific families of threats contributed to the steep rise in the malware infection rates of Austria, Germany, Italy, and the Netherlands: Win32/EyeStye, Win32/Zbot (also known as Zeus), Win32/Keygen, and Blacole.",
        answers: ["Blacole"]
      }, {
        id: "Jwhfvg",
        text: "If the Jokra packer is limited to the one group, then the connections between Backdoor.Prioxer and Trojan.Jokra are reliable.",
        answers: ["Jokra"]
      }, {
        id: "K7AQ0b",
        text: "If the file, detected as TrojanDownloader:Win32/Filcout.A, is loaded in a computer with a vulnerability exploited by Blacole, it may download and run arbitrary files.",
        answers: ["Blacole"]
      }, {
        id: "LlfA_6",
        text: "Instead of redirecting to innocent pages with Google adware or porn affiliate site, it takes you to a site which pushes malware (the malware is Zlob related, and detected by Sophos as Troj/Zlobar-Fam ).",
        answers: ["Zlob"]
      }]
    });
  });

  sessionRouter.put('/:id', function(req, res) {
    console.log({body: req.body})
    console.log({worker_id: req.param('worker_id')})
    console.log({answers: req.param('answers')})
    console.log({body: req.body})
    console.log({params: req.params})
    res.send({
      'session': {
        id: 'XXXX',
        questions: ["J3Xq5m", "JNFAmM", "Jwhfvg", "K7AQ0b", "LlfA_6"],
        worker_id: 'w123',
        task_id: 'test123',
        questions_type: "boolean"
      },
      'questions': [{
        id: "J3Xq5m",
        text: "For more than two decades, our research teams from Slovakia, Russia, Canada, Netherlands, Latin America and the US worked on hundreds of projects uncovering series of events related to hackers and other cyber criminals activities including less worrying samples to sophisticated and targeted attacks such as ACAD projects stealthy ACAD/Medre, military focused Georgian Georbot, very first impactful mac Flashback Trojan or the Linux/Cdorked.A apache webserver backdoor, analyzing their methodology and tracking their origins as well as the malware spread, helping users, companies and government institutions around the world to stay and feel protected.",
        answers: ["ACAD/Medre"]
      }, {
        id: "JNFAmM",
        text: "Four specific families of threats contributed to the steep rise in the malware infection rates of Austria, Germany, Italy, and the Netherlands: Win32/EyeStye, Win32/Zbot (also known as Zeus), Win32/Keygen, and Blacole.",
        answers: ["Blacole"]
      }, {
        id: "Jwhfvg",
        text: "If the Jokra packer is limited to the one group, then the connections between Backdoor.Prioxer and Trojan.Jokra are reliable.",
        answers: ["Jokra"]
      }, {
        id: "K7AQ0b",
        text: "If the file, detected as TrojanDownloader:Win32/Filcout.A, is loaded in a computer with a vulnerability exploited by Blacole, it may download and run arbitrary files.",
        answers: ["Blacole"]
      }, {
        id: "LlfA_6",
        text: "Instead of redirecting to innocent pages with Google adware or porn affiliate site, it takes you to a site which pushes malware (the malware is Zlob related, and detected by Sophos as Troj/Zlobar-Fam ).",
        answers: ["Zlob"]
      }]
    });
  });

  sessionRouter.delete('/:id', function(req, res) {
    res.status(204).end();
  });

  app.use('/api/sessions', sessionRouter);
};

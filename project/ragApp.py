import time
import streamlit as st
from typing import List, Dict
from queryMaker import QueryMaker


queryMaker = QueryMaker()


def render_top(top_k: List[Dict], key):
    # Store expanded state only if not already present

    with st.expander("Retrival Details", expanded=True):
        options = dict(
            {
                f"ID {record['source_id']} | Score: {round(record['score'], 3)}": record
                for record in top_k
            }
        )

        selected = st.selectbox(
            "Select a retrieved resume:", list(options.keys()), key=key
        )

        record = options[selected]
        with st.container(height=400):
            st.markdown(record["resume"])


def generator():
    res = "message that will be sent every time"
    for x in res.split():
        yield x + " "
        time.sleep(0.05)


def respond(prompt):
    # res = {
    #     "text": generator(),
    #     "top_k": [
    #         {
    #             "score": 0.5330118807493779,
    #             "source_id": 74,
    #             "resume": "SKILLS: - 1) Team leading 2) Self-motivated 3) Hard working     Strengths: Ready to learn new Programming Languages, Punctual, Discipline, Respectfulness. DECLARATION:- I hereby inform you that all the statement made above are true with the best of my knowledge and belief. Education Details \r\nAugust 2014 to July 2017 MCA Computer Sciene Amravati, Maharashtra SGBAU, Amaravti\r\nJava Web Developer \r\n\r\n\r\nSkill Details \r\nCore Java,JSP,Servlet,Spring,Hibernate,Struts,Javascript- Exprience - 6 monthsCompany Details \r\ncompany - Salcluster Technologies\r\ndescription - 1.  I am Java web developer\r\n2. Jsp , servlet, Sprinng MVC Technologies",
    #         },
    #         {
    #             "score": 0.5357470070972945,
    #             "source_id": 115,
    #             "resume": "Total IT Experience 15 years. Core expertise in Data Base Design, PHP, Python, MySql, JavaScript, HTML 5, Ajax, Jquery, XML, Agile Methodology, DevOps Methodology, Scrum Framework, JIRA Tool, GIT, Bitbucket, Anjular JS 1, Angular JS 2, Core Java, J2EE. Education Details \r\nApril 2004 MCM Computer Management Pune, Maharashtra Pune University\r\nApril 1998 B.Sc Maths  Kerala University\r\nProject Manager \r\n\r\nProject Manager\r\nSkill Details \r\nData Base Design, PHP, Python, MySql, JavaScript, HTML, Ajax, XML, Agile Methodology, DevOps Methodology, Scrum Framework, JIRA Tool, GIT, Bitbucket, Jquery,  AngularJs, Amazon MWS , Bootstrap, Node.js, Laravel, Scrum- Exprience - 120 monthsCompany Details \r\ncompany - Knoxed Infotech Pvt. Ltd.\r\ndescription -     Client interaction\r\n    Maintain work processes\r\n    Creates project plans through Agile Model & Methodology\r\n    Maintains project objectives\r\n    Working with multi-profiled teams of technical and non technical stakeholders\r\n    Monitors production and quality to customer/stakeholder/sponsor standards\r\n    Conduct office management tasks\r\n    Ensuring that the day-to-day operations of the business run smoothly\r\n    Introducing key performance indicators (KPI's) and ensuring that these measurements are tracked\r\nand reviewed on a regular basis\r\n    Prepare, revise and submit weekly-monthly reports, budgets and other documentation as\r\nnecessary\r\n    Document current policies and procedures in all departments as well as implement new procedures\r\nfor improvement\r\n    Maintain smooth running of the office, filling in where needed\r\n    Implement quality management and regulatory compliance strategies\r\n    Dealing with HR related tasks\r\n    Administering payroll\r\n    Perform training sessions\r\n    Regular meetings with Top Management\r\nProject Undertaken : Internal ERP system For Knoxed Ltd, UK, With PHP, Mysql, Ajax, XML,\r\nAmazon AWS, Raspberry pi Server, Python.\r\ncompany - Venturus International\r\ndescription -     Client interaction\r\n    Creates project plans through Agile Model & Methodology\r\n    Manage team   s workload and workflow\r\n    Allocate and track resources as required\r\n    Set and monitor deadlines\r\n    QC\r\n    Maintain tasks and jobs on task management system\r\n    Conduct research and development\r\n    Create new systems, databases and websites as necessary\r\nProject Undertaken : Internal ERP system For Knoxed Ltd, UK, With PHP, Mysql, Ajax, XML,\r\nAmazon AWS\r\ncompany - SmashingDay\r\ndescription -     Client interaction\r\n    Creates project plans through Agile Model & Methodology\r\n    Manage team   s workload and workflow\r\n    Allocate and track resources as required\r\n    Set and monitor deadlines\r\n    Project documentation\r\n    Conduct and maintain appraisals and progress of each employee\r\n    Adhere to deadlines as necessary\r\n    Maintain work logs\r\n    Conduct research and development\r\n    Create new systems, databases and websites as necessary\r\nProject Undertaken :\r\na) www.SmashingDay.com\r\nb) www.viralsocials.com\r\ncompany - Xento Systems Pvt. Ltd\r\ndescription -     Client interaction\r\n    Creates project plans through Agile Model & Methodology\r\n    Manage team   s workload and workflow\r\n    Allocate and track resources as required\r\n    Set and monitor deadlines\r\n    QC\r\n    Maintain tasks and jobs on task management system\r\n    Conduct research and development\r\n    Create new systems, databases and websites as necessary\r\nProject Undertaken :\r\na) www.familylink.com\r\nb) www.propertysolutions.com\r\nc) www.speedyceus.com\r\nd) www.ceus-nursing.com\r\ncompany - STP Global Solutions Pvt. Ltd.\r\ndescription -     Client interaction\r\n    Creates project plans through Agile Model & Methodology\r\n    Manage team   s workload and workflow\r\n    Allocate and track resources as required\r\n    Set and monitor deadlines\r\n    Conduct and maintain appraisals and progress of each employee\r\n    QC\r\n    Maintain tasks and jobs on task management system\r\n    Conduct research and development\r\n    Create new systems, databases and websites as necessary\r\nProject Undertaken :\r\na) www.stplafricaonline.com\r\nb) www.stplafrica.com\r\nc) www.1stexpert.com\r\nd) www.jcca-net.org\r\ne) www.rimsys.eu\r\nf) www.prayerlister.org\r\ncompany - Promark Infotech Pvt. Ltd\r\ndescription -     Development & Design\r\n    Create new systems, databases and websites as necessary\r\nProject Undertaken :\r\na) www.justbe.com/\r\nb) www.mtpian.com/\r\nc) www.sababa.nl/booking/\r\nd) www.physicaltherapy-hiu.com\r\ncompany - 7cees Group\r\ndescription -     Development & Design\r\n    Create new systems, databases and websites as necessary\r\nProject Undertaken :\r\na) Golwin-reality\r\nb) Maza",
    #         },
    #         {
    #             "score": 0.5607426530762337,
    #             "source_id": 39,
    #             "resume": "Education Details \r\nJanuary 2016 B.Sc. Information Technology Mumbai, Maharashtra University of Mumbai\r\nJanuary 2012 HSC  Allahabad, Uttar Pradesh Allahabad university\r\nJanuary 2010 SSC dot Net Allahabad, Uttar Pradesh Allahabad university\r\nWeb designer and Developer Trainer \r\n\r\nWeb designer and Developer\r\nSkill Details \r\nWeb design- Exprience - 12 months\r\nPhp- Exprience - 12 monthsCompany Details \r\ncompany - NetTech India\r\ndescription - Working. ( salary - 12k)\r\nPERSONAL INTEREST\r\n\r\nListening to Music, Surfing net, Watching Movie, Playing Cricket.\r\ncompany - EPI Center Academy\r\ndescription - Working.  ( Salary Contract based)\r\ncompany - Aptech Charni Road\r\ndescription - Salary Contract based)",
    #         },
    #         {
    #             "score": 0.5626319359650793,
    #             "source_id": 68,
    #             "resume": "Education Details \r\n BE IT   pjlce\r\nJava Developer \r\n\r\nJava Developer\r\nSkill Details \r\nc++- Exprience - Less than 1 year months\r\nc- Exprience - Less than 1 year months\r\nJAVA- Exprience - Less than 1 year months\r\nDS- Exprience - Less than 1 year months\r\nJdbc- Exprience - 24 months\r\nHibernate- Exprience - Less than 1 year months\r\nJava J2Ee- Exprience - Less than 1 year months\r\nJavascript- Exprience - 6 months\r\nJQuery- Exprience - 6 months\r\nAjax- Exprience - 6 monthsCompany Details \r\ncompany - Almighty tech pvt ltd nagpur\r\ndescription - 1. As a Java Developer.\r\n    ORGANISATION: Almighty tech pvt ltd Nagpur\r\n    DESIGNATION.: Java Developer.\r\n    DURATION.: From 1st jan 2018\r\n    Notice Period: 15 days\r\nJOB RESPONSIBILITIES\r\n    Resolve Bugs\r\n    Develop project as per user requirement.\r\n\r\nKNOWLEDGE ABOUT:-\r\n    Programming language C, C++, DS, Java(Swing, JDBC, J2EE) java script,jquery,Ajax\r\n    Ms office, Excel.",
    #         },
    #         {
    #             "score": 0.5632983476263428,
    #             "source_id": 105,
    #             "resume": "Education Details \r\nJune 2013 to June 2016 Diploma Computer science Pune, Maharashtra Aissms\r\nJune 2016 BE pursuing Computer science Pune, Maharashtra Anantrao pawar college of Engineering & Research centre\r\nPython Developer \r\n\r\n\r\nSkill Details \r\nCompany Details \r\ncompany - Cybage Software Pvt. Ltd\r\ndescription - I want to work in organisation as a python developer to utilize my knowledge & To gain more knowledge with our organisation.",
    #         },
    #     ],
    # }
    # return res
    return queryMaker.query(prompt)


st.title("Resume Screener Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []


main = st.empty()
with main.container():
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "top_k" in msg:
                render_top(msg["top_k"], i)


if prompt := st.chat_input("Try me!"):
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        res = respond(prompt)
        text = st.write_stream(res["text"])
        key = len(st.session_state.messages)
        render_top(res["top_k"], key)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": text,
                "top_k": res["top_k"],
                "key": key,
            }
        )

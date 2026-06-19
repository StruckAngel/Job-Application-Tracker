# Packages
import os, llm
from db import add_job
from datetime import date
from openai import OpenAI
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Footer, Label, Input, ContentSwitcher, Button, Markdown

# Sets workign directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Variables
today = str(date.today())
jobStatus = ["In Progress", "Ghosted", " Rejected"]

# Should Replace this if your using another MODEL
MODEL = "deepseek-reasoner"

# Markdown applications
with open ("Job-Application-List.md", "r") as f:
    applicationMarkdown = f.read()

# The system prompt
with open("system.md", "r") as f:
    SYSTEM = f.read()

# Markdown for the user prompt
class Prompt(Markdown):
    pass

# markdown for LLM 
class Response(Markdown):
    pass

def add_job_md(companyName, positionName, jobCity, jobState, jobSite, jobStatus, jobDescription, today):

    text = (f"+ {companyName} -- {positionName} -- {jobCity} -- {jobState} -- {jobStatus[0]} -- {today}\n")

    # writes into markdown file
    with open("Job-Application-List.md", "a") as f:
        f.write(text)

    text = (f"{companyName}-{positionName}-{today}")

    #Archieve job description
    with open(f"description/{text}", "w") as f:
        f.write(jobDescription)

# textual
class JobApplication(App):

    CSS_PATH = "main.tcss"

    BINDINGS = [
        Binding(
            key="0",
            action="show('home')",
            description="Home",
        ),
        Binding(
            key="1",
            action="show('input')",
            description="Input",
        ),
        Binding(
            key="2",
            action="show('applicationsMD')",
            description="Applications MD",
        ),
        Binding(
            key="ctrl+z", 
            action="quit", 
            description="Exit",
            key_display="ctrl+z",
        ),
        Binding(
            key="Question_mark",
            action="help",
            description="Help",
            key_display="?",
        )
    ]

    def compose(self) -> ComposeResult:

        yield Footer()

        with ContentSwitcher(initial="home"):

            with Vertical(id="home"):
                yield Label("Job Application Tracker")
                yield Button (label="Input Forum", id="inputCN")
                yield Button (label="Applications", id="applicationsCN")
                yield Button(label="AI Helper", id="aiHelperCN")

            with Vertical(id="input"):
                with VerticalScroll():
                    yield Label ("Company:")
                    yield Input(id="companyName") 
                    yield Label ("Position:")
                    yield Input (id="positionName")
                    yield Label ("City:")
                    yield Input(id="jobCity")
                    yield Label ("State:")
                    yield Input(id="jobState")
                    yield Label ("Site:")
                    yield Input (id="jobSite")
                    yield Label("Description:")
                    yield Input(id="jobDescription")
                    yield Button(label="Enter",id="enter")

            with Vertical(id="applicationsMD"):
                yield Markdown(applicationMarkdown)


            with Vertical (id="aiHelper"):
                with VerticalScroll(id="chat-view"):
                    yield Response("INTERFACE 2037 READY FOR INQUIRY")
                yield Input(placeholder="How can I help you?", id="aiInput")




    def on_mount(self) -> None:
        self.model = llm.get_model(MODEL)
        # Anchors the text box
        self.query_one("#chat-view").anchor()


    # Takes "Return" input
    @on(Input.Submitted, "#aiInput")
    async def on_input(self, event: Input.Submitted) -> None:
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        await chat_view.mount(Prompt(event.value))
        await chat_view.mount(response := Response())
        self.send_prompt(event.value, response)

    # Gets response
    @work(thread=True)
    def send_prompt(self, prompt: str, response: Response) -> None:

        response_content = ""
        llm_response = self.model.prompt(prompt, system=SYSTEM)
        for chunk in llm_response:
            response_content += chunk
            self.call_from_thread(response.update, response_content)
            

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "enter":
            companyName = self.query_one("#companyName", Input).value
            positionName = self.query_one("#positionName", Input).value
            jobCity = self.query_one("#jobCity",Input).value
            jobState = self.query_one("#jobState",Input).value
            jobSite = self.query_one("#jobSite",Input).value
            jobDescription = self.query_one("#jobDescription",Input).value
            
            add_job(companyName, positionName, jobCity, jobState, jobSite, jobStatus, jobDescription, today)
            add_job_md(companyName, positionName, jobCity, jobState, jobSite, jobStatus, jobDescription, today)
            
            self.log(locals())
            
            # Clears inputs
            self.query_one("#companyName", Input).clear()
            self.query_one("#positionName", Input).clear()
            self.query_one("#jobCity", Input).clear()
            self.query_one("#jobState", Input).clear()
            self.query_one("#jobSite", Input).clear()
            self.query_one("#jobDescription", Input).clear()

        # Button conent switcher
        if event.button.id == "inputCN":
            self.app.action_show("input")

        if event.button.id == "applicationsCN":
            self.app.action_show("applicationsMD")

        if event.button.id == "aiHelperCN":
            self.app.action_show("aiHelper")

    # Required for navigation 
    def action_show(self, page: str) -> None:
        self.query_one(ContentSwitcher).current = page

if __name__ == "__main__":
    app = JobApplication()
    app.run()



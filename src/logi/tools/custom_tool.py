from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pandas as pd
import resend, os
from dotenv import load_dotenv
load_dotenv()

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
# Custom tool for the mailing agent
class MailingAgentToolInput(BaseModel):
    """Input schema for MailingAgentTool."""
    # content: str = Field(..., description="Content of the email to be sent.")
    vendors: list = Field(..., description="List of vendor email addresses.")

class MailingAgentTool(BaseTool):
    name: str = "Mailing Agent Tool"
    description: str = (
        "This tool sends emails to vendors with the provided content."
    )
    args_schema: Type[BaseModel] = MailingAgentToolInput

    def _run(self, content, vendors: list):
        resend_api_key = os.getenv("RESEND_API_KEY")
        if not resend_api_key:
            raise ValueError("RESEND_API_KEY environment variable is not set.") 
        
        resend.api_key = resend_api_key
        
        params: resend.Emails.SendParams = {
            "from": "Acme <onboarding@resend.dev>",
            "to": vendors,
            "subject": "Request for material",
            "html": content,
        }
        response = resend.Emails.send(params)
        return response

# Defining a custom tool for the calculation
class SupplierScoringToolInput(BaseModel):
    """Input schema for CarrierScoringTool."""
    csv_path: str = Field(..., description="Path to the CSV file containing carrier data.")

class SupplierScoringTool(BaseTool):
    name: str = "Carrier Scoring Tool"
    description: str = (
        "This tool scores carriers based on historical performance data."
    )
    args_schema: Type[BaseModel] = SupplierScoringToolInput

    def _run(self, csv_path: str) -> pd.DataFrame:
        """
        Create a supplier scorecard from the provided CSV file.
        Args:
            file_path (str): Path to the CSV file containing supplier data.
        Returns:
            pd.DataFrame: A DataFrame containing the supplier scorecard.
        """
        df = pd.read_csv(csv_path)
        
        required_cols = ['SupplierName', 'OnTimeDelivery', 'DefectRate', 'SupplierRating']
        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        scorecard = df[required_cols].copy()
        print("Historical supplier data:\n", scorecard)

        # Convert 'OnTimeDelivery' and 'DefectRate' to numerical values
        for row in scorecard.index:
            scorecard.at[row, 'OnTimeDelivery'] = 1 if scorecard.at[row, 'OnTimeDelivery'] == 'Yes' else 0
            scorecard.at[row, 'DefectRate'] = 1 if scorecard.at[row, 'DefectRate'] == 'High' else 0  # assuming 'High' = 1, 'Low' = 0

        # Calculate the final score
        for row in scorecard.index:
            scorecard.at[row, 'FinalScore'] = (
                scorecard.at[row, 'OnTimeDelivery'] * 0.5 +
                (1 - scorecard.at[row, 'DefectRate']) * 0.3 +
                scorecard.at[row, 'SupplierRating'] * 0.2
            )

        # Group by 'SupplierName' and calculate the average score
        scorecard = scorecard.drop(columns=['OnTimeDelivery', 'DefectRate', 'SupplierRating'])
        scorecard = scorecard.groupby('SupplierName').mean().reset_index()
        scorecard = scorecard.sort_values(by='FinalScore', ascending=False)

        return scorecard
        

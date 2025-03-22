import logging
from typing import Dict

import openai

logger = logging.getLogger(__name__)


class SummaryGenerator:
    def __init__(self, openai_api_key: str):
        self.client = openai.OpenAI(api_key=openai_api_key)

    def generate(self, transcript_text: str, episode_info: Dict) -> str:
        """Generate a summary of the transcript."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a helpful assistant that helps parents understand the podcast episode, in an actionable way.
                        You will be provided with a transcript of the episode, which will contain timestamps for each segment. Here's an example:

                        ```
                        [00:00:00] This is the first segment
                        [00:01:00] This is the second segment
                        ```

                        You must include these timestamps to reference specific parts of the transcript (with a timestamped link to the episode) in your response. For example:

                        ```
                        - **Bullet point**: Some example of a bullet point. [¹](https://link.to.episode/abc123?t=25m55s) [²](https://link.to.episode/abc123?t=56s) [³](https://link.to.episode/abc123?t=1h2m0s)
                        - **Another bullet point**: More exampling. [¹](https://link.to.episode/abc123?t=25m55s) [²](https://link.to.episode/abc123?t=56s)
                        ```

                        Make sure you're not repeating information in your response.
                        Never say "the hosts", always use the names of the hosts, which are Nick and Billy.
                        Never include a closing note in your response.
                        
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"""
                        You should provide:
                        1. A thorough summary of the episode.
                        2. If there are research backed concepts that get emphasized in the episode that seemed particularly impactful, include them. Be selective to the most important ones.
                        3. A cheat sheet for parents to help them understand the episode and apply the learnings to their own lives.
                        
                        If it's a reflections episode (one were listeners send questions), also include a section for all the questions and answers. 
                        Don't oversimplify neither the questions nor the answers. 
                        Make sure to include the short and the long questions in the order in which they are asked in the transcript.
                        
                        The cheat sheet should be concise and to the point, and should be formatted as a list of bullet points.
                        Don't include the episode title in your response.

                        Here's the link to the episode:
                        {episode_info["link"]}

                        Here is the transcript:
                        
                        ``` 
                        {transcript_text}
                        ```
                        """,
                    },
                ],
                temperature=0,
                max_tokens=4000,
            )
            print(f"Tokens used: {response.usage.total_tokens}")

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return None

# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="📗 Pocketbook",
        page_icon="👋",
    )

    st.write("# 📗 Welcome to Pocketbook")

    st.markdown(
        """
        
        **👨🏻‍💻 I built Pocketbook to give myself a personal finance tool** after
        [Mint shut down](https://www.cnbc.com/select/mint-app-shutting-down-what-users-should-do/)
        at the end of 2023. 

        ➕ **This tool combines** data visualization with AI to streamline analysis

        **👈 Check out the pages on the side bar**, or read about them below
        
        **📊 Analyze** allows me to connect to, filter, visualize, and chat wtih my spending data.

        **💬 Upload** allows me to upload any CSV file and use natural language to query it
        
        
        
    """
    )


if __name__ == "__main__":
    run()

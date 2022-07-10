import React from 'react';
import { VERSION } from '@twilio/flex-ui';
import { FlexPlugin } from '@twilio/flex-plugin';

import CustomTaskListContainer from './components/CustomTaskList/CustomTaskList.Container';
import reducers, { namespace } from './states';

const PLUGIN_NAME = 'SamplePlugin';

export default class SamplePlugin extends FlexPlugin {
  constructor() {
    super(PLUGIN_NAME);
  }

  /**
   * This code is run when your plugin is being started
   * Use this to modify any UI components or attach to the actions framework
   *
   * @param flex { typeof import('@twilio/flex-ui') }
   * @param manager { import('@twilio/flex-ui').Manager }
   */
  async init(flex, manager) {
    this.registerReducers(manager);

    const options = { sortOrder: -1 };
    flex.AgentDesktopView.Panel1.Content.add(<CustomTaskListContainer key="SamplePlugin-component" />, options);
	let alertSound = new Audio("https://adtestsite.xyz/sound/beep.mp3");
    alertSound.loop = true;
  
    const resStatus = ["accepted","canceled","rejected","rescinded","timeout"];
  
    manager.workerClient.on("reservationCreated", function(reservation) {
      if (reservation.task.taskChannelUniqueName === 'voice') {
        alertSound.play()
	    };
		  resStatus.forEach((e) => {
	        reservation.on(e, () => {
		      alertSound.pause()
		    });
	    });
    });
  }
  
  /**
   * Registers the plugin reducers
   *
   * @param manager { Flex.Manager }
   */
  registerReducers(manager) {
    if (!manager.store.addReducer) {
      // eslint-disable-next-line
      console.error(`You need FlexUI > 1.9.0 to use built-in redux; you are currently on ${VERSION}`);
      return;
    }

    manager.store.addReducer(namespace, reducers);
  }
}

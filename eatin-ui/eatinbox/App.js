import React, {Component} from 'react';
import { StatusBar } from 'react-native';
import {Provider} from 'react-redux';
import {createStore, applyMiddleware, combineReducers} from 'redux'
import thunk from 'redux-thunk';
import {createAppContainer, createStackNavigator} from 'react-navigation'

import menuListReducer from './src/store/reducers/menuList';   
import userReducer from './src/store/reducers/userReducer'

import IntroductionScreen from './src/screens/Introduction/IntroductionScreen'
import VenderInfoScreen from './src/screens/VenderInfo/VenderInfoScreen';
import FoodScreen from './src/screens/Food/FoodScreen';
import CartScreen from './src/screens/Cart/CartScreen';
import CurrentOrderScreen from './src/screens/Orders/Current/CurrentOrderScreen';
// import PastOrderScreen from './src/screens/Orders/Past/PastOrderScreen'
import FilterScreen from './src/screens/Filter/FilterScreen';
import RegisterScreen from './src/screens/Register/RegisterScreen';
import LoginScreen from './src/screens/Login/LoginScreen';

// import Playground from './src/screens/Playground/Playground'

const rootReducer = combineReducers({
  register : userReducer,
  menuList: menuListReducer,
})

const store = createStore(rootReducer, applyMiddleware(thunk))


export default class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <StatusBar backgroundColor="black" barStyle="light-content" />
        <AppContainer/>
      </Provider>
    );
  }
}


const rootStack = createStackNavigator(
  {
    Introduction: IntroductionScreen,
    Vendor: VenderInfoScreen,
    Cart: CartScreen,
    CurrentOrderScreen: CurrentOrderScreen,
    Register: RegisterScreen,
    FilterScreen: FilterScreen,
    Login: LoginScreen,
    Menu: FoodScreen,
    // Play: Playground,
  },

  {
    initialRouteName: 'Menu',
    defaultNavigationOptions: {
      // transitionConfig: () => fromRight(),
      header: null,
    }
  }
)

const AppContainer = createAppContainer(rootStack)
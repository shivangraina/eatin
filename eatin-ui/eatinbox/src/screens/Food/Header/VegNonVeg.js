import React, { Component } from 'react';

import {
    View,
    StyleSheet,
    Text,
    TouchableWithoutFeedback,
    Animated
} from 'react-native';

export default class VegNonVeg extends Component {
    constructor(props) {
        super(props)
    }

    state= {
        toggle: false,
        animation: new Animated.Value(0),
        bgColor: '#96ff45',
    }

    startAnimation = () => {
        this.setState(
            (state) => { 
                const bgColor = state.toggle ? '#96ff45' : '#a8a8a8'

                return {  
                    toggle: !state.toggle,
                    bgColor,
                }
            }, 
        
            () => {
                const value = this.state.toggle ? 17 : 0;
                Animated.spring(this.state.animation, {
                    toValue: value,
                }).start()
        })
    }

    render() {
        const vegButtonAni = {
            toggleAni: {
                transform: [
                    {
                        translateX : this.state.animation,
                    }
                ]
            },

            buttonBgColor: {
                backgroundColor: this.state.bgColor,
            }            
        }

        return (
            <View style={styles.container}>
                <Text style={styles.vegText}>VEG</Text>
                <View style={styles.buttonCont}>
                    <TouchableWithoutFeedback onPress={this.startAnimation}>
                        <View style={[styles.vegButton, vegButtonAni.buttonBgColor]}>
                            <Animated.View style={[styles.toggleButtonCont, vegButtonAni.toggleAni]}>

                            </Animated.View>
                        </View>
                    </TouchableWithoutFeedback>
                </View>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flexDirection: 'column',
        borderWidth:0,
    },

    vegText: {
        fontSize: 8,
        color: '#000', 
        fontWeight: 'bold',
        borderWidth:0,
        textAlign: 'center',
    },

    buttonCont:{
        borderWidth:0,
    },

    vegButton: {
        width: 35,
        height: 17,
        borderWidth:0,
        borderRadius: 17,
        backgroundColor: '#96ff45',
    },

    toggleButtonCont:{
        borderWidth:1,
        width:17,
        height:17,
        borderRadius:17,
        backgroundColor: '#fff',

    }
});